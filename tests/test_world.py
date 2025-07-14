# ==============================
# tests/test_world.py
# ==============================
'''
# Este arquivo contém testes unitários para a classe World do projeto Wumpus World.
# O objetivo é garantir que o mundo seja inicializado corretamente e que seus principais
# atributos estejam presentes e com os tipos esperados.
# 
# Explicação dos testes:
# - Verifica se o tamanho do mundo está correto.
# - Verifica se os atributos essenciais (posição do agente, ouro, wumpus e poços) existem.
# - Verifica se os tipos desses atributos são os esperados (tupla para posições, lista para poços).
# 
# Esses testes ajudam a garantir que a classe World está pronta para ser utilizada pelos agentes.
'''
import os
import pytest
from world.world import World

# Configurações de diretório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(BASE_DIR, "logs", "run")  # Diretório de saída para logs

def test_world_initialization():
    # Cria um mundo de tamanho 4x4 com uma semente fixa para resultados reprodutíveis
    world = World(size=4, seed=42)
    # Verifica se o tamanho do mundo está correto
    assert world.size == 4
    # Verifica se os principais atributos existem
    assert hasattr(world, "agent_pos")
    assert hasattr(world, "gold_pos")
    assert hasattr(world, "wumpus_pos")
    assert hasattr(world, "pits")
    # Verifica se os tipos dos atributos são os esperados
    assert isinstance(world.agent_pos, tuple)
    assert isinstance(world.gold_pos, tuple)
    assert isinstance(world.wumpus_pos, tuple)
    assert isinstance(world.pits, list)
