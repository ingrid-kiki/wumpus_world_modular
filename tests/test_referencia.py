# ==============================
# tests/test_referencia.py
# ==============================
"""
# Garante que os resultados do projeto não mudam sem uma decisão explícita.
# O cenário e como atualizá-lo em uma mudança intencional estão em tests/referencia.py.
"""

import json
from collections import Counter

import pytest

from tests import referencia

AVISO = (
    "Os resultados de referência mudaram. Se NÃO era a intenção, há uma regressão. "
    "Se era, rode 'python -m tests.referencia' e explique o motivo no commit e no CHANGELOG."
)


@pytest.fixture(scope="module")
def atual():
    return referencia.calcular()


@pytest.fixture(scope="module")
def esperado():
    return json.loads(referencia.ARQUIVO.read_text(encoding="utf-8"))


def test_mundos_gerados_nao_mudam(atual, esperado):
    assert atual["mundos"] == esperado["mundos"], AVISO


@pytest.mark.parametrize("agente", list(referencia.AGENTES))
def test_resultados_do_agente_nao_mudam(agente, atual, esperado):
    filtrar = lambda dados: [e for e in dados["execucoes"] if e["agente"] == agente]  # noqa: E731
    assert filtrar(atual) == filtrar(esperado), AVISO


def test_regras_do_fitness_nao_mudam(atual, esperado):
    assert atual["casos_de_fitness"] == esperado["casos_de_fitness"], AVISO


def test_decisoes_do_agente_logico_nao_mudam(atual, esperado):
    assert atual["casos_do_agente_logico"] == esperado["casos_do_agente_logico"], AVISO


def test_referencia_cobre_o_que_promete(esperado):
    """Protege o próprio cenário: precisa ter os mundos e agentes declarados, com resultados variados."""
    tamanhos = len(referencia.TAMANHOS)
    por_agente = Counter(e["agente"] for e in esperado["execucoes"])
    assert len(esperado["mundos"]) == tamanhos * len(referencia.SEMENTES)
    assert por_agente["logico"] == tamanhos * len(referencia.SEMENTES_LOGICO)
    assert por_agente["genetico"] == por_agente["aleatorio"] == tamanhos * len(referencia.SEMENTES)
    assert set(Counter(e["status"] for e in esperado["execucoes"])) >= {"vitoria", "morte"}


def test_referencia_detecta_mudanca(atual, esperado):
    """O hash do histórico precisa acusar qualquer diferença nas ações."""
    alterado = dict(atual["execucoes"][0], historico="0" * 16)
    assert alterado != esperado["execucoes"][0]
