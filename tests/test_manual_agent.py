# ==============================
# tests/test_manual_agent.py
# ==============================
"""
# Este arquivo contém testes unitários para o agente ManualAgent do projeto Wumpus World.
# O objetivo é garantir que o agente manual recebe corretamente uma instância do mundo
# e armazena essa referência em seu atributo 'world'.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente manual (ManualAgent) passando o mundo criado.
# - Verifica se o agente possui o atributo 'world'.
# - Verifica se o atributo 'world' do agente é exatamente o objeto mundo criado.
#
# Esse teste assegura que o agente manual está pronto para interagir com o ambiente.
"""

from agents.manual_agent import ManualAgent
from world.world import World


def test_manual_agent_receives_world():
    # Cria um mundo de tamanho 4x4 com semente fixa
    world = World(size=4, seed=42)
    # Cria o agente manual passando o mundo
    agent = ManualAgent(world)
    # Verifica se o agente possui o atributo 'world'
    assert hasattr(agent, "world")
    # Verifica se o atributo 'world' do agente é o mesmo objeto criado
    assert agent.world == world
