# ==============================
# tests/test_world.py
# ==============================
"""
# Este arquivo contém testes unitários para a classe Mundo do projeto Wumpus World.
# O objetivo é garantir que o mundo seja inicializado corretamente e que seus principais
# atributos estejam presentes e com os tipos esperados.
#
# Explicação dos testes:
# - Verifica se o tamanho do mundo está correto.
# - Verifica se os atributos essenciais (posição do agente, ouro, wumpus e poços) existem.
# - Verifica se os tipos desses atributos são os esperados (tupla para posições, lista para poços).
#
# Esses testes ajudam a garantir que a classe Mundo está pronta para ser utilizada pelos agentes.
"""

from world.world import Mundo


def test_criacao_do_mundo():
    # Cria um mundo de tamanho 4x4 com uma semente fixa para resultados reprodutíveis
    mundo = Mundo(tamanho=4, semente=42)
    # Verifica se o tamanho do mundo está correto
    assert mundo.tamanho == 4
    # Verifica se os principais atributos existem
    assert hasattr(mundo, "posicao_agente")
    assert hasattr(mundo, "posicao_ouro")
    assert hasattr(mundo, "posicao_wumpus")
    assert hasattr(mundo, "pocos")
    # Verifica se os tipos dos atributos são os esperados
    assert isinstance(mundo.posicao_agente, tuple)
    assert isinstance(mundo.posicao_ouro, tuple)
    assert isinstance(mundo.posicao_wumpus, tuple)
    assert isinstance(mundo.pocos, list)
