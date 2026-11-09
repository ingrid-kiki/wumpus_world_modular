# ==============================
# tests/test_genetic_agent.py
# ==============================
"""
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
"""

from agents.genetic_agent import GeneticAgent
from world.world import World
from tests.conftest import GA_RAPIDO


def test_genetic_agent_initialization():
    # Cria um mundo de tamanho 4x4 com semente fixa
    world = World(size=4, seed=42)
    # Cria o agente genético com parâmetros customizados
    agent = GeneticAgent(world, **GA_RAPIDO)

    # Testa se os atributos principais existem
    assert hasattr(agent, "world")
    assert hasattr(agent, "ga")
    assert hasattr(agent, "history")

    # Verifica se a instância de algoritmo genético foi criada corretamente
    assert agent.ga.pop_size == GA_RAPIDO["population_size"]
    assert agent.ga.gens == GA_RAPIDO["gens"]
    assert agent.ga.chrom_length == GA_RAPIDO["chrom_length"]

    # Verifica se o histórico está vazio inicialmente
    assert agent.history == []

    # Executa o método run e verifica o retorno
    result = agent.run()
    assert isinstance(result, dict)
    assert "history" in result
    assert "dados_extra" in result
    assert "fitness" in result["dados_extra"]
