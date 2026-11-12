# ==============================
# tests/test_distribuicao_das_acoes.py
# ==============================
"""
# Este arquivo contém um teste unitário para analisar a distribuição das ações
# executadas pelo agente genético (AgenteGenetico) durante uma simulação no mundo Wumpus.
#
# O objetivo é garantir que o agente está realmente executando ações e permitir
# uma análise didática da variedade de decisões tomadas pelo algoritmo genético.
#
# Explicação do teste:
# - Cria uma instância do mundo (Mundo) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (AgenteGenetico) passando o mundo criado.
# - Executa o agente e obtém o resultado da simulação.
# - Extrai a lista de ações executadas do histórico retornado.
# - Conta a frequência de cada ação usando Counter.
# - Imprime a distribuição das ações para análise didática.
# - Garante que pelo menos uma ação foi executada (teste básico de funcionamento).
"""

from collections import Counter

from agents.genetic_agent import AgenteGenetico
from tests.conftest import GA_RAPIDO
from world.world import Mundo


def test_distribuicao_das_acoes():
    # Cria o mundo e o agente genético
    mundo = Mundo(tamanho=4, semente=42)
    agente = AgenteGenetico(mundo, **GA_RAPIDO)
    # Executa o agente e obtém o resultado
    result = agente.executar()
    # Extrai as ações do histórico
    actions = [h["acao"] for h in result["historico"]]
    # Conta a frequência de cada ação
    count = Counter(actions)

    # Imprime a distribuição das ações para análise didática
    print("📊 Distribuição de ações:", dict(count))
    assert len(actions) > 0
