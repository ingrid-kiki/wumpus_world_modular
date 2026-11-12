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
from agents.random_search_agent import RandomSearchAgent
from ga.individual import Individual
from world.world import World


def acoes(resultado):
    return [p["acao"] for p in resultado["historico"]]


def test_mesma_semente_mesmo_resultado_sem_depender_do_random_global():
    execucoes = []
    for lixo in (1, 2):
        random.seed(lixo)
        execucoes.append(acoes(RandomSearchAgent(World(size=4, seed=3), avaliacoes=200, chrom_length=20).run()))
    assert execucoes[0] == execucoes[1]


def test_executa_a_melhor_sequencia_e_respeita_o_orcamento(monkeypatch):
    avaliacoes = []
    original = Individual.evaluate

    def contar(self, world):
        avaliacoes.append(1)
        return original(self, world)

    monkeypatch.setattr(Individual, "evaluate", contar)
    w = World(size=4, seed=1)
    resultado = RandomSearchAgent(w, avaliacoes=300, chrom_length=20).run()
    assert len(avaliacoes) == 300
    assert w.won or not w.is_alive or len(resultado["historico"]) == 20


def test_fitness_informado_corresponde_a_sequencia_executada():
    w = World(size=4, seed=2)
    referencia = w.clone()
    resultado = RandomSearchAgent(w, avaliacoes=300, chrom_length=20).run()
    individuo = Individual(0)
    individuo.chromosome = acoes(resultado)
    individuo.evaluate(referencia)
    assert individuo.fitness == resultado["fitness"]


def test_orcamento_zero_ainda_avalia_uma_sequencia():
    assert RandomSearchAgent(World(size=4, seed=0), avaliacoes=0, chrom_length=5).avaliacoes == 1


def test_benchmark_usa_o_mesmo_orcamento_do_ag(tmp_path):
    pasta = tmp_path / "run"
    _, df = main.rodar_benchmark(
        [
            "--agentes",
            "aleatorio",
            "genetico",
            "--sizes",
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
    meta = json.loads((pasta / "metadata.json").read_text(encoding="utf-8"))
    assert meta["parametros_busca_aleatoria"] == {"chrom_length": 15, "avaliacoes": 50}
    assert not (pasta / "advanced_charts_aleatorio_4x4").exists()  # não tem dados extras
    assert len(pd.read_csv(pasta / "resultados_benchmark.csv")) == 2


def test_orcamento_explicito_tem_prioridade(tmp_path):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        [
            "--agentes",
            "aleatorio",
            "--sizes",
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
    meta = json.loads((pasta / "metadata.json").read_text(encoding="utf-8"))
    assert meta["parametros_busca_aleatoria"] == {"chrom_length": 5, "avaliacoes": 7}
