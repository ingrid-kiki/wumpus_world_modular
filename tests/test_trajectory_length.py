# ==============================
# tests/test_trajectory_length.py
# ==============================
'''
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
'''

import os
import pytest
from datetime import datetime
from agents.genetic_agent import GeneticAgent
from world.world import World

# Obtém o diretório base onde o script está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Cria um timestamp único para os logs
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Cria um diretório de saída para os logs, com um timestamp único
output_dir = os.path.join(BASE_DIR, "logs", f"run_{timestamp}")

def test_action_sequence_length():
    # Cria o mundo e o agente genético
    world = World(size=4, seed=42)
    agent = GeneticAgent(world)
    # Executa o agente e obtém o resultado
    result = agent.run()
    # Extrai o histórico de ações executadas
    trajectory = result["history"]

    # Imprime o número de ações executadas para análise didática
    print(f"🔁 Número de ações executadas: {len(trajectory)}")
    # Garante que pelo menos uma ação foi executada
    assert len(trajectory) > 0
