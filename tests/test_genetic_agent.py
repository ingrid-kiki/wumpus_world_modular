# ==============================
# tests/test_genetic_agent.py
# ==============================
"""
# Este arquivo contém testes unitários para o agente AgenteGenetico do projeto Wumpus World.
# O objetivo é garantir que o agente genético é inicializado corretamente, possui os principais
# atributos e integra corretamente o núcleo do algoritmo genético (AlgoritmoGenetico).
#
# Explicação dos testes:
# - Cria uma instância do mundo (Mundo) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (AgenteGenetico) com parâmetros customizados.
# - Verifica se o agente possui os atributos essenciais: 'mundo', 'ag' (núcleo do GA) e 'history'.
# - Verifica se os parâmetros do núcleo do GA (população, gerações, cromossomo) estão corretos.
# - Garante que o histórico do agente está vazio ao iniciar.
# - Executa o método 'run' do agente e verifica se o retorno é um dicionário com as chaves esperadas.
#
# Esses testes asseguram que o agente genético está pronto para ser utilizado em simulações e benchmarks.
"""

from agents.genetic_agent import AgenteGenetico
from tests.conftest import GA_RAPIDO
from world.world import Mundo


def test_criacao_do_agente_genetico():
    # Cria um mundo de tamanho 4x4 com semente fixa
    mundo = Mundo(tamanho=4, semente=42)
    # Cria o agente genético com parâmetros customizados
    agente = AgenteGenetico(mundo, **GA_RAPIDO)

    # Testa se os atributos principais existem
    assert hasattr(agente, "mundo")
    assert hasattr(agente, "ag")
    assert hasattr(agente, "historico")

    # Verifica se a instância de algoritmo genético foi criada corretamente
    assert agente.ag.tamanho_populacao == GA_RAPIDO["tamanho_populacao"]
    assert agente.ag.geracoes == GA_RAPIDO["geracoes"]
    assert agente.ag.tamanho_cromossomo == GA_RAPIDO["tamanho_cromossomo"]

    # Verifica se o histórico está vazio inicialmente
    assert agente.historico == []

    # Executa o método run e verifica o retorno
    result = agente.executar()
    assert isinstance(result, dict)
    assert "historico" in result
    assert "dados_extra" in result
    assert "fitness" in result["dados_extra"]
