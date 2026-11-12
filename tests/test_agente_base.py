# ==============================
# tests/test_agente_base.py
# ==============================
"""
# Testes da classe base Agente e da lista única de agentes: todo agente herda de Agente,
# devolve o resultado no formato único e é encontrado pelo mesmo dicionário em todo o programa.
"""

import contextlib
import io

import pytest

import benchmark
import main
from agents.agente import Agente
from agents.registro import AGENTES_AUTOMATICOS, AGENTES_DISPONIVEIS
from world.world import World

PARAMETROS_RAPIDOS = {
    "logico": {},
    "logico_seguro": {},
    "genetico": {"population_size": 10, "gens": 3, "chrom_length": 10},
    "aleatorio": {"avaliacoes": 20, "chrom_length": 10},
}
CHAVES_DO_PASSO = {"passo", "acao", "percepcao", "status", "posicao"}


def mundo_com_ouro_ao_lado():
    """Mundo 4x4 com o ouro em (0, 1) e o Wumpus e os poços longe do agente."""
    mundo = World(size=4, seed=0)
    mundo.gold_pos, mundo.wumpus_pos, mundo.pits = (0, 1), (3, 3), [(3, 0), (2, 2)]
    return mundo


def test_agente_e_abstrato():
    with pytest.raises(TypeError):
        Agente(World(size=4, seed=0))


@pytest.mark.parametrize("nome", list(AGENTES_DISPONIVEIS))
def test_todos_os_agentes_herdam_de_agente(nome):
    assert issubclass(AGENTES_DISPONIVEIS[nome], Agente)


@pytest.mark.parametrize("nome", AGENTES_AUTOMATICOS)
def test_resultado_tem_o_formato_unico(nome):
    mundo = World(size=4, seed=3)
    with contextlib.redirect_stdout(io.StringIO()):
        resultado = AGENTES_DISPONIVEIS[nome](mundo, **PARAMETROS_RAPIDOS[nome]).run()
    assert {"historico", "passos", "dados_extra"} <= set(resultado)
    assert resultado["passos"] == len(resultado["historico"]) > 0
    assert all(set(passo) == CHAVES_DO_PASSO for passo in resultado["historico"])
    assert [passo["passo"] for passo in resultado["historico"]] == list(range(1, resultado["passos"] + 1))
    assert resultado["historico"][-1]["posicao"] == list(mundo.agent_pos)


def test_agente_manual_devolve_o_formato_unico(monkeypatch):
    respostas = iter(["DIREITA", "AGARRAR"])
    monkeypatch.setattr("builtins.input", lambda *_: next(respostas))
    mundo = mundo_com_ouro_ao_lado()
    with contextlib.redirect_stdout(io.StringIO()):
        resultado = AGENTES_DISPONIVEIS["manual"](mundo).run()
    assert [passo["acao"] for passo in resultado["historico"]] == ["DIREITA", "AGARRAR"]
    assert resultado["historico"][-1]["status"] == "GANHOU" and resultado["dados_extra"] == {}


def test_executar_sequencia_para_no_fim_do_jogo():
    class Executor(Agente):
        def run(self):
            self.executar_sequencia(["DIREITA", "AGARRAR", "BAIXO"])
            return self.resultado(extra=1)

    resultado = Executor(mundo_com_ouro_ao_lado()).run()
    assert [passo["acao"] for passo in resultado["historico"]] == ["DIREITA", "AGARRAR"]
    assert resultado["historico"][0]["posicao"] == [0, 1] and resultado["extra"] == 1


def test_main_e_benchmarks_usam_a_mesma_lista():
    for modulo in (main, benchmark):
        assert modulo.AGENTES_DISPONIVEIS is AGENTES_DISPONIVEIS
