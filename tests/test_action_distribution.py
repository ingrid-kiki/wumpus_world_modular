# ==============================
# tests/test_action_distribution.py
# ==============================
"""
# Este arquivo contém um teste unitário para analisar a distribuição das ações
# executadas pelo agente genético (GeneticAgent) durante uma simulação no mundo Wumpus.
#
# O objetivo é garantir que o agente está realmente executando ações e permitir
# uma análise didática da variedade de decisões tomadas pelo algoritmo genético.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (GeneticAgent) passando o mundo criado.
# - Executa o agente e obtém o resultado da simulação.
# - Extrai a lista de ações executadas do histórico retornado.
# - Conta a frequência de cada ação usando Counter.
# - Imprime a distribuição das ações para análise didática.
# - Garante que pelo menos uma ação foi executada (teste básico de funcionamento).
"""

from collections import Counter
from agents.genetic_agent import GeneticAgent
from world.world import World
from tests.conftest import GA_RAPIDO


def test_action_distribution():
    # Cria o mundo e o agente genético
    world = World(size=4, seed=42)
    agent = GeneticAgent(world, **GA_RAPIDO)
    # Executa o agente e obtém o resultado
    result = agent.run()
    # Extrai as ações do histórico
    actions = [h["ação"] for h in result["history"]]
    # Conta a frequência de cada ação
    count = Counter(actions)

    # Imprime a distribuição das ações para análise didática
    print("📊 Distribuição de ações:", dict(count))
    assert len(actions) > 0
