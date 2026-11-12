# ==============================
# tests/test_busca_aleatoria.py
# ==============================
"""
# Testes do agente de busca aleatória, referência para o agente genético (#31).
"""

import json
import random

import pandas as pd

import main
from agents.random_search_agent import AgenteAleatorio
from ga.individual import Individuo
from world.world import Mundo


def acoes(resultado):
    return [p["acao"] for p in resultado["historico"]]


def test_mesma_semente_mesmo_resultado_sem_depender_do_random_global():
    execucoes = []
    for lixo in (1, 2):
        random.seed(lixo)
        execucoes.append(
            acoes(AgenteAleatorio(Mundo(tamanho=4, semente=3), avaliacoes=200, tamanho_cromossomo=20).executar())
        )
    assert execucoes[0] == execucoes[1]


def test_executa_a_melhor_sequencia_e_respeita_o_orcamento(monkeypatch):
    avaliacoes = []
    original = Individuo.avaliar

    def contar(self, mundo):
        avaliacoes.append(1)
        return original(self, mundo)

    monkeypatch.setattr(Individuo, "avaliar", contar)
    w = Mundo(tamanho=4, semente=1)
    resultado = AgenteAleatorio(w, avaliacoes=300, tamanho_cromossomo=20).executar()
    assert len(avaliacoes) == 300
    assert w.ganhou or not w.agente_vivo or len(resultado["historico"]) == 20


def test_fitness_informado_corresponde_a_sequencia_executada():
    w = Mundo(tamanho=4, semente=2)
    referencia = w.clonar()
    resultado = AgenteAleatorio(w, avaliacoes=300, tamanho_cromossomo=20).executar()
    individuo = Individuo(0)
    individuo.cromossomo = acoes(resultado)
    individuo.avaliar(referencia)
    assert individuo.fitness == resultado["fitness"]


def test_orcamento_zero_ainda_avalia_uma_sequencia():
    assert AgenteAleatorio(Mundo(tamanho=4, semente=0), avaliacoes=0, tamanho_cromossomo=5).avaliacoes == 1


def test_benchmark_usa_o_mesmo_orcamento_do_ag(tmp_path):
    pasta = tmp_path / "run"
    _, df = main.rodar_benchmark(
        [
            "--agentes",
            "aleatorio",
            "genetico",
            "--tamanhos",
            "4",
            "--execucoes",
            "2",
            "--populacao",
            "10",
            "--geracoes",
            "5",
            "--cromossomo",
            "15",
            "--saida",
            str(pasta),
        ]
    )
    assert list(df["agente"]) == ["aleatorio", "genetico"]
    assert df["erros"].sum() == 0
    meta = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    assert meta["parametros_busca_aleatoria"] == {"tamanho_cromossomo": 15, "avaliacoes": 50}
    assert not (pasta / "graficos_avancados_aleatorio_4x4").exists()  # não tem dados extras
    assert len(pd.read_csv(pasta / "resultados_benchmark.csv")) == 2


def test_orcamento_explicito_tem_prioridade(tmp_path):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        [
            "--agentes",
            "aleatorio",
            "--tamanhos",
            "4",
            "--execucoes",
            "1",
            "--avaliacoes",
            "7",
            "--cromossomo",
            "5",
            "--saida",
            str(pasta),
        ]
    )
    meta = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    assert meta["parametros_busca_aleatoria"] == {"tamanho_cromossomo": 5, "avaliacoes": 7}
