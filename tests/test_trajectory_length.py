# ==============================
# tests/test_trajectory_length.py
# ==============================
"""
# Este arquivo contém um teste unitário para verificar o comprimento da trajetória (sequência de ações)
# executada pelo agente genético (GeneticAgent) no ambiente Wumpus World.
#
# O objetivo é garantir que o agente realmente executa uma sequência de ações durante a simulação,
# ou seja, que o histórico de ações não está vazio.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (GeneticAgent) passando o mundo criado.
# - Executa o agente e obtém o resultado da simulação.
# - Extrai o histórico de ações executadas (trajectory) do resultado.
# - Imprime o número de ações executadas para análise didática.
# - Garante que pelo menos uma ação foi executada (histórico não vazio).
"""

from agents.genetic_agent import GeneticAgent
from tests.conftest import GA_RAPIDO
from world.world import World


def test_action_sequence_length():
    # Cria o mundo e o agente genético
    world = World(size=4, seed=42)
    agent = GeneticAgent(world, **GA_RAPIDO)
    # Executa o agente e obtém o resultado
    result = agent.run()
    # Extrai o histórico de ações executadas
    trajectory = result["historico"]

    # Imprime o número de ações executadas para análise didática
    print(f"🔁 Número de ações executadas: {len(trajectory)}")
    # Garante que pelo menos uma ação foi executada
    assert len(trajectory) > 0
