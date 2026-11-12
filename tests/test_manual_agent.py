# ==============================
# tests/test_manual_agent.py
# ==============================
"""
# Este arquivo contém testes unitários para o agente AgenteManual do projeto Wumpus World.
# O objetivo é garantir que o agente manual recebe corretamente uma instância do mundo
# e armazena essa referência em seu atributo 'mundo'.
#
# Explicação do teste:
# - Cria uma instância do mundo (Mundo) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente manual (AgenteManual) passando o mundo criado.
# - Verifica se o agente possui o atributo 'mundo'.
# - Verifica se o atributo 'mundo' do agente é exatamente o objeto mundo criado.
#
# Esse teste assegura que o agente manual está pronto para interagir com o ambiente.
"""

from agents.manual_agent import AgenteManual
from world.world import Mundo


def test_agente_manual_recebe_o_mundo():
    # Cria um mundo de tamanho 4x4 com semente fixa
    mundo = Mundo(tamanho=4, semente=42)
    # Cria o agente manual passando o mundo
    agente = AgenteManual(mundo)
    # Verifica se o agente possui o atributo 'mundo'
    assert hasattr(agente, "mundo")
    # Verifica se o atributo 'mundo' do agente é o mesmo objeto criado
    assert agente.mundo == mundo
