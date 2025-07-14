# ==============================
# tests/test_logic_agent.py
# ==============================
'''
# Este arquivo contém testes unitários para o agente LogicAgent do projeto Wumpus World.
# O objetivo é garantir que o agente lógico é inicializado corretamente e possui os principais
# atributos e métodos necessários para operar no ambiente.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente lógico (LogicAgent) passando o mundo criado.
# - Verifica se o agente possui o atributo 'world' (referência ao ambiente).
# - Verifica se o agente possui o atributo 'knowledge' (base de conhecimento lógica).
# - Verifica se o agente possui o método 'decide' (responsável por decidir a próxima ação).
#
# Esses testes asseguram que o agente lógico está pronto para ser utilizado em simulações e benchmarks.
'''

import os
import pytest
from agents.logic_agent import LogicAgent
from world.world import World
from datetime import datetime

# Configurações de diretório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(BASE_DIR, "logs", f"run_{timestamp}")

def test_logic_agent_initialization():
    # Cria um mundo de tamanho 4x4 com semente fixa
    world = World(size=4, seed=42)
    # Cria o agente lógico passando o mundo
    agent = LogicAgent(world)
    # Verifica se o agente possui o atributo 'world'
    assert hasattr(agent, "world")
    # Verifica se o agente possui o atributo 'knowledge'
    assert hasattr(agent, "knowledge")
    # Verifica se o agente possui o método 'decide'
    assert hasattr(agent, "decide")
