# ==============================
# tests/test_visualizer.py
# ==============================
"""
# Testes da janela que reproduz a partida (visual/visualizer.py) e da pergunta no menu.
# A janela roda com o pygame em modo sem tela, então os testes funcionam no CI.
"""

import contextlib
import io
import os
import sys

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import main  # noqa: E402
from agents.logico_seguro import AgenteLogicoSeguro  # noqa: E402
from visual.visualizer import CORES, Visualizador  # noqa: E402
from world.world import Mundo  # noqa: E402


def test_reproducao_chega_ao_mesmo_estado_final_da_partida():
    mundo = Mundo(tamanho=4, semente=3)
    inicial = mundo.clonar()
    with contextlib.redirect_stdout(io.StringIO()):
        historico = AgenteLogicoSeguro(mundo).executar()["historico"]
    mostrados = Visualizador(inicial).reproduzir(historico, passos_por_segundo=0, esperar_fechar=False)
    assert mostrados == len(historico)
    assert (inicial.posicao_agente, inicial.ganhou, inicial.agente_vivo, inicial.wumpus_vivo) == (
        mundo.posicao_agente,
        mundo.ganhou,
        mundo.agente_vivo,
        mundo.wumpus_vivo,
    )


def test_janela_pinta_o_agente_na_casa_dele():
    mundo = Mundo(tamanho=4, semente=1)
    janela = Visualizador(mundo)
    janela.desenhar_mundo()
    x, y = mundo.posicao_agente
    meio = (y * janela.tamanho_casa + janela.tamanho_casa // 2, x * janela.tamanho_casa + janela.tamanho_casa // 2)
    assert tuple(janela.tela.get_at(meio))[:3] == CORES["agente"]
    janela.reproduzir([], passos_por_segundo=0, esperar_fechar=False)


@pytest.mark.parametrize("resposta, abre", [("s", True), ("sim", True), ("", False)])
def test_menu_so_abre_a_janela_quando_pedido(resposta, abre, monkeypatch):
    respostas = iter(["4", "1", resposta])
    monkeypatch.setattr("builtins.input", lambda *_: next(respostas))
    abertas = []
    monkeypatch.setattr(main, "mostrar_partida", lambda inicial, historico: abertas.append((inicial, historico)))
    with contextlib.redirect_stdout(io.StringIO()):
        main.execucao_unica("logico")
    assert bool(abertas) == abre
    if abre:
        inicial, historico = abertas[0]
        assert inicial.posicao_agente == (0, 0) and historico  # a janela recebe o mundo do início e a partida jogada


def test_sem_pygame_a_janela_so_avisa(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "visual.visualizer", None)  # faz o import falhar
    main.mostrar_partida(Mundo(tamanho=4, semente=0), [])
    assert "Não foi possível abrir a janela" in capsys.readouterr().out
