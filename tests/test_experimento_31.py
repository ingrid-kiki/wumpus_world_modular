# ==============================
# tests/test_experimento_31.py
# ==============================
"""
# Testes do script de comparação da issue #31 (experimentos/comparar_metodos.py).
"""

import pandas as pd
import pytest

from experimentos import comparar_metodos as exp
from ga.ga_core import AlgoritmoGenetico
from world.world import Mundo


def mundo_fixo(pocos, ouro=(1, 1)):
    w = Mundo(tamanho=3, semente=0)
    w.pocos, w.posicao_ouro, w.posicao_wumpus = pocos, ouro, (2, 2)
    return w


def test_resolvivel_reconhece_caminho_e_bloqueio():
    assert exp.resolvivel(mundo_fixo([(0, 1)]))
    assert not exp.resolvivel(mundo_fixo([(0, 1), (1, 0)]))


def test_venceu_e_fitness_real_usam_o_mundo_sem_altera_lo():
    w = mundo_fixo([(0, 2)])
    assert exp.venceu(w, ["DIREITA", "BAIXO", "AGARRAR"])
    assert not exp.venceu(w, ["DIREITA", "AGARRAR"])
    assert exp.fitness_real(w, ["DIREITA", "BAIXO", "AGARRAR"]) > 0
    assert w.posicao_agente == (0, 0) and not w.ganhou


def test_holm_ajusta_na_ordem_original():
    assert exp.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_comparar_conta_mundos_discordantes():
    linhas = [
        {"metodo": m, "mundo": 4, "genes": 10, "orcamento": 50, "semente": s, "vitoria": v}
        for s, (a, b) in enumerate([(True, True), (True, False), (True, False), (False, False)])
        for m, v in (("busca_aleatoria", a), ("ag_projeto", b))
    ]
    r = exp.comparar(pd.DataFrame(linhas)).iloc[0]
    assert (r.vitorias_aleatoria, r.vitorias_metodo, r.so_aleatoria_venceu, r.so_metodo_venceu) == (3, 1, 2, 0)
    assert r.p == pytest.approx(0.5)


def test_variante_truncamento_e_o_ag_do_projeto():
    """Sem variações, AGVariante precisa dar exatamente o mesmo resultado do AlgoritmoGenetico."""
    args = (20, 8, 20, 0.05, 0.8)
    w = Mundo(tamanho=4, semente=2)
    original = AlgoritmoGenetico(*args, semente=2).executar(w)["melhor"].cromossomo
    variante = exp.AGVariante(*args, semente=2).executar(w)["melhor"].cromossomo
    assert variante == original


def test_orcamento_do_ag_nao_e_ultrapassado():
    w = Mundo(tamanho=4, semente=1)
    _, extra = exp.genetico(w, 400, 20, 1)
    assert 0 <= extra["repetidas"] <= 1
    ag = exp.AGVariante(40, 400 // 40 - 1, 20, 0.02, 0.8, semente=1)
    ag.executar(w)
    assert ag.avaliacoes + ag.acertos_cache <= 400


def test_tentar_devolve_uma_linha_completa():
    linha = exp.tentar("busca_aleatoria", 4, 10, 20, 0)
    assert {"metodo", "vitoria", "fitness", "resolvivel"} <= set(linha)
