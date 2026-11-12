# ==============================
# tests/test_proximidade.py
# ==============================
"""
# Testes do bônus de proximidade ao ouro no fitness do AG (#31).
"""

import json

import pytest

import main
from agents.genetic_agent import AgenteGenetico
from ga.ga_core import AlgoritmoGenetico
from ga.individual import Individuo
from world.world import Mundo


def mundo():
    """Mundo 5x5: ouro em (4,4), poço em (2,2), Wumpus em (4,0). Distância máxima: 8."""
    w = Mundo(tamanho=5, semente=0)
    w.posicao_ouro, w.pocos, w.posicao_wumpus = (4, 4), [(2, 2)], (4, 0)
    return w


def nota(cromossomo, proximidade=0.0):
    ind = Individuo(0)
    ind.cromossomo = list(cromossomo)
    ind.avaliar(mundo(), proximidade)
    return ind.fitness


def test_peso_zero_mantem_o_fitness_original():
    cromossomo = ["DIREITA", "BAIXO", "TIRO"]
    ind = Individuo(0)
    ind.cromossomo = cromossomo
    ind.avaliar(mundo())
    assert nota(cromossomo, 0.0) == ind.fitness


def test_bonus_cresce_com_a_proximidade():
    longe = nota(["CIMA"], 20.0) - nota(["CIMA"])  # distância 8: bônus 0
    perto = nota(["DIREITA", "DIREITA"], 20.0) - nota(["DIREITA", "DIREITA"])  # distância 6
    assert longe == pytest.approx(0.0)
    assert perto == pytest.approx(20 * (1 - 6 / 8))


def test_bonus_usa_a_menor_distancia_alcancada():
    """Afastar-se depois não tira o bônus de ter chegado perto."""
    ida = ["DIREITA", "DIREITA"]
    volta = ida + ["ESQUERDA", "ESQUERDA"]
    assert nota(volta, 20.0) - nota(volta) == pytest.approx(20 * (1 - 6 / 8))


def test_bonus_conta_ate_a_morte():
    cromossomo = ["BAIXO", "BAIXO", "DIREITA", "DIREITA"]  # morre no poço em (2,2): distância 4
    assert nota(cromossomo, 20.0) - nota(cromossomo) == pytest.approx(20 * (1 - 4 / 8))


def test_ag_sem_proximidade_nao_muda():
    w = Mundo(tamanho=4, semente=2)
    a = AlgoritmoGenetico(20, 8, 20, 0.05, 0.8, semente=2).executar(w)["melhor"].cromossomo
    b = AlgoritmoGenetico(20, 8, 20, 0.05, 0.8, semente=2, proximidade=0.0).executar(w)["melhor"].cromossomo
    assert a == b


def test_agente_com_proximidade_e_reprodutivel():
    execucoes = [
        [
            p["acao"]
            for p in AgenteGenetico(
                Mundo(tamanho=6, semente=4), tamanho_populacao=20, geracoes=10, tamanho_cromossomo=30, proximidade=20.0
            ).executar()["historico"]
        ]
        for _ in range(2)
    ]
    assert execucoes[0] == execucoes[1]


def test_opcao_chega_ao_agente_e_aos_metadados(tmp_path):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        [
            "--agentes",
            "genetico",
            "--tamanhos",
            "4",
            "--execucoes",
            "1",
            "--populacao",
            "10",
            "--geracoes",
            "3",
            "--cromossomo",
            "10",
            "--proximidade",
            "20",
            "--saida",
            str(pasta),
        ]
    )
    meta = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    assert meta["parametros_ag"]["proximidade"] == 20.0


def test_sem_a_opcao_o_padrao_e_o_fitness_original(tmp_path):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        [
            "--agentes",
            "genetico",
            "--tamanhos",
            "4",
            "--execucoes",
            "1",
            "--populacao",
            "10",
            "--geracoes",
            "3",
            "--cromossomo",
            "10",
            "--saida",
            str(pasta),
        ]
    )
    meta = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    assert meta["parametros_ag"]["proximidade"] == 0.0


def test_peso_negativo_e_recusado(capsys):
    with pytest.raises(SystemExit):
        main.criar_parser().parse_args(["--proximidade", "-1"])
    assert "precisa ser 0 ou maior" in capsys.readouterr().err
