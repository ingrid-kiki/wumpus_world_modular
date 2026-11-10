# ==============================
# tests/test_final_status.py
# ==============================
"""
# Este arquivo contém um teste unitário para verificar o status final do agente genético (GeneticAgent)
# após a execução de uma simulação no ambiente Wumpus World.
#
# O objetivo é garantir que o agente termina a simulação em um dos estados esperados:
# "MORTO", "GANHOU" ou "OK". Isso ajuda a validar que o ciclo de vida do agente está
# sendo registrado corretamente e que o histórico de execução está consistente.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (GeneticAgent) passando o mundo criado.
# - Executa o agente e obtém o resultado da simulação.
# - Extrai o status final do agente a partir do último elemento do histórico.
# - Imprime o status final para análise didática.
# - Garante que o status final está entre os valores esperados.
"""

from agents.genetic_agent import GeneticAgent
from tests.conftest import GA_RAPIDO
from world.world import World


def test_final_agent_status():
    # Cria o mundo e o agente genético
    world = World(size=4, seed=42)
    agent = GeneticAgent(world, **GA_RAPIDO)
    # Executa o agente e obtém o resultado
    result = agent.run()
    # Extrai o status final do histórico de execução
    last_status = result["history"][-1]["status"]

    # Imprime o status final para análise didática
    print(f"🎯 Status final: {last_status}")
    # Garante que o status final é um dos esperados
    assert last_status in ["MORTO", "GANHOU", "OK"]
