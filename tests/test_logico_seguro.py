# ==============================
# tests/test_logico_seguro.py
# ==============================
"""
# Testes do agente logico_seguro: as deduções da base de conhecimento, a ordem das regras,
# os números medidos na investigação de 11/11/2026 e o registro do agente no programa.
"""

import contextlib
import io

import pandas as pd
import pytest

import benchmark
import main
from agents.logico_seguro import AgenteLogicoSeguro, BaseConhecimentoSegura
from world.world import Mundo


def base_com(tamanho, visitadas, atual):
    """Base de conhecimento com as casas visitadas ({posição: percepção}) e a posição atual."""
    kb = BaseConhecimentoSegura(tamanho=tamanho)
    for pos, percepcao in visitadas.items():
        kb.conhecidas[pos] = {"seguro": not percepcao, "visitado": True, "percepcoes": percepcao}
        kb.visitas[pos] = 1
    kb.posicao_atual = atual
    return kb


# ---------------------------------------------------------------- Deduções


def test_vizinhas_de_casa_sem_brisa_sao_seguras():
    kb = base_com(3, {(0, 0): []}, (0, 0))
    assert kb.casas_seguras() == {(0, 0), (0, 1), (1, 0)}


def test_brisa_nao_torna_as_vizinhas_seguras():
    kb = base_com(3, {(0, 0): ["BRISA"]}, (0, 0))
    assert kb.casas_seguras() == {(0, 0)}


def test_poco_certo_quando_so_uma_casa_explica_a_brisa():
    # (0,1) sente brisa; (1,1) é segura por causa de (1,0); só sobra (0,2) para ter o poço
    kb = base_com(3, {(0, 0): [], (0, 1): ["BRISA"], (1, 0): []}, (0, 1))
    seguras = kb.casas_seguras()
    assert kb.poco_certo((0, 2), seguras)
    assert not kb.poco_certo((1, 1), seguras)


def test_poco_nao_e_certo_com_duas_explicacoes():
    kb = base_com(3, {(0, 0): [], (0, 1): ["BRISA"]}, (0, 1))
    assert not kb.poco_certo((0, 2), kb.casas_seguras())


# ---------------------------------------------------------------- Decisão


def test_brilho_e_fedor_vem_antes_de_andar():
    assert BaseConhecimentoSegura(tamanho=4).inferir_acao(["BRILHO", "FEDOR", "BRISA"]) == "AGARRAR"
    assert BaseConhecimentoSegura(tamanho=4).inferir_acao(["FEDOR", "BRISA"]) == "TIRO"


def test_prefere_casa_segura_a_casa_suspeita():
    # Em (0,1) com brisa: (0,2) é suspeita, (1,1) é segura por causa de (1,0)
    kb = base_com(3, {(0, 0): [], (1, 0): []}, (0, 1))
    assert kb.inferir_acao(["BRISA"]) == "BAIXO"


def test_anda_ate_casa_segura_distante_por_casas_visitadas():
    # Em (0,2) com brisa: nenhuma vizinha nova é segura, mas (2,0) é, e o caminho volta por (0,1)
    kb = base_com(3, {(0, 0): [], (1, 0): [], (0, 1): [], (1, 1): ["BRISA"]}, (0, 2))
    assert kb.inferir_acao(["BRISA"]) == "ESQUERDA"


def test_sem_casa_segura_arrisca_e_nunca_escolhe_poco_certo():
    # Em (0,0) com brisa num mundo 2x2: (0,1) e (1,0) são igualmente suspeitas; nenhuma é poço certo
    kb = base_com(2, {}, (0, 0))
    assert kb.inferir_acao(["BRISA"]) in ("BAIXO", "DIREITA")
    # Em (0,1): (0,2) é poço certo (única explicação da brisa de (0,1)) e (2,1) só é suspeita.
    # As duas têm a mesma suspeita; sem o descarte do poço certo, o desempate escolheria (0,2).
    kb = base_com(3, {(0, 0): [], (0, 1): ["BRISA"], (1, 0): [], (1, 1): ["BRISA"]}, (0, 1))
    seguras = kb.casas_seguras()
    assert kb.poco_certo((0, 2), seguras)
    assert not kb.poco_certo((2, 1), seguras)
    assert kb.arriscar({(0, 2), (2, 1)}, seguras) == "BAIXO"


def test_sem_nada_a_fazer_fica_em_casas_conhecidas():
    kb = base_com(2, {(0, 0): ["BRISA"], (0, 1): ["BRISA"]}, (0, 1))
    kb.conhecidas[(1, 0)] = {"seguro": False, "visitado": True, "percepcoes": ["BRISA"]}
    kb.conhecidas[(1, 1)] = {"seguro": False, "visitado": True, "percepcoes": ["BRISA"]}
    assert kb.inferir_acao(["BRISA"]) in ("ESQUERDA", "BAIXO")


# ---------------------------------------------------------------- Resultados


# Medidos no agente implementado, com desempate pela posição (docs/investigacao-agente-logico-2026-11.md, seção 8),
# sementes 0 a 999: vitórias e mortes por tamanho
NUMEROS_DA_INVESTIGACAO = {4: (834, 164), 6: (864, 136), 8: (919, 81)}


@pytest.mark.parametrize("tamanho", sorted(NUMEROS_DA_INVESTIGACAO))
def test_reproduz_os_numeros_registrados(tamanho):
    vitorias = mortes = 0
    for semente in range(1000):
        mundo = Mundo(tamanho=tamanho, semente=semente)
        with contextlib.redirect_stdout(io.StringIO()):
            AgenteLogicoSeguro(mundo).executar()
        vitorias += mundo.ganhou
        mortes += not mundo.agente_vivo
    assert (vitorias, mortes) == NUMEROS_DA_INVESTIGACAO[tamanho]


def test_nunca_morre_pelo_wumpus():
    for semente in range(300):
        mundo = Mundo(tamanho=6, semente=semente)
        with contextlib.redirect_stdout(io.StringIO()):
            AgenteLogicoSeguro(mundo).executar()
        assert mundo.agente_vivo or mundo.posicao_agente != mundo.posicao_wumpus


# ---------------------------------------------------------------- Registro no programa


@pytest.mark.parametrize("modulo", [main, benchmark])
def test_registrado_no_programa_e_nos_benchmarks(modulo):
    assert modulo.AGENTES_DISPONIVEIS["logico_seguro"] is AgenteLogicoSeguro


def test_roda_num_benchmark_pela_linha_de_comando(tmp_path):
    with contextlib.redirect_stdout(io.StringIO()):
        main.rodar_benchmark(
            ["--agentes", "logico", "logico_seguro", "--tamanhos", "4", "--execucoes", "5", "--saida", str(tmp_path)]
        )
    df = pd.read_csv(tmp_path / "resultados_benchmark.csv")
    assert list(df["agente"]) == ["logico", "logico_seguro"]
    assert (df[["vitorias", "mortes", "sobreviveu", "erros"]].sum(axis=1) == 5).all()
