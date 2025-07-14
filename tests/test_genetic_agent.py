# ==============================
# tests/test_genetic_agent.py
# ==============================
'''
# Este arquivo contém testes unitários para o agente GeneticAgent do projeto Wumpus World.
# O objetivo é garantir que o agente genético é inicializado corretamente, possui os principais
# atributos e integra corretamente o núcleo do algoritmo genético (GeneticAlgorithm).
#
# Explicação dos testes:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (GeneticAgent) com parâmetros customizados.
# - Verifica se o agente possui os atributos essenciais: 'world', 'ga' (núcleo do GA) e 'history'.
# - Verifica se os parâmetros do núcleo do GA (população, gerações, cromossomo) estão corretos.
# - Garante que o histórico do agente está vazio ao iniciar.
# - Executa o método 'run' do agente e verifica se o retorno é um dicionário com as chaves esperadas.
#
# Esses testes asseguram que o agente genético está pronto para ser utilizado em simulações e benchmarks.
'''

import os
import pytest
from agents.genetic_agent import GeneticAgent
from ga.ga_core import GeneticAlgorithm
from world.world import World

# Configuração do diretório de saída para logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
timestamp = "20231004_1200"  # Exemplo de timestamp, deve ser gerado dinamicamente em um caso real
output_dir = os.path.join(BASE_DIR, "logs", f"run_{timestamp}")

def test_genetic_agent_initialization():
    # Cria um mundo de tamanho 4x4 com semente fixa
    world = World(size=4, seed=42)
    # Cria o agente genético com parâmetros customizados
    agent = GeneticAgent(world, population_size=30, gens=50, chrom_length=10)

    # Testa se os atributos principais existem
    assert hasattr(agent, "world")
    assert hasattr(agent, "ga")
    assert hasattr(agent, "history")

    # Verifica se a instância de algoritmo genético foi criada corretamente
    assert agent.ga.pop_size == 30
    assert agent.ga.gens == 50
    assert agent.ga.chrom_length == 10
    
    # Verifica se o histórico está vazio inicialmente
    assert agent.history == []

    # Executa o método run e verifica o retorno
    result = agent.run()
    assert isinstance(result, dict)
    assert "history" in result
    assert "fitness" in result
