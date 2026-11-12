# ==============================
# tests/test_logic_agent.py
# ==============================
"""
# Este arquivo contém testes unitários para o agente AgenteLogico do projeto Wumpus World.
# O objetivo é garantir que o agente lógico é inicializado corretamente e possui os principais
# atributos e métodos necessários para operar no ambiente.
#
# Explicação do teste:
# - Cria uma instância do mundo (Mundo) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente lógico (AgenteLogico) passando o mundo criado.
# - Verifica se o agente possui o atributo 'mundo' (referência ao ambiente).
# - Verifica se o agente possui o atributo 'conhecimento' (base de conhecimento lógica).
# - Verifica se o agente possui o método 'decidir_acao' (responsável por decidir a próxima ação).
#
# Esses testes asseguram que o agente lógico está pronto para ser utilizado em simulações e benchmarks.
"""

from agents.logic_agent import AgenteLogico
from world.world import Mundo


def test_criacao_do_agente_logico():
    # Cria um mundo de tamanho 4x4 com semente fixa
    mundo = Mundo(tamanho=4, semente=42)
    # Cria o agente lógico passando o mundo
    agente = AgenteLogico(mundo)
    # Verifica se o agente possui o atributo 'mundo'
    assert hasattr(agente, "mundo")
    # Verifica se o agente possui o atributo 'conhecimento'
    assert hasattr(agente, "conhecimento")
    # Verifica se o agente possui o método 'decidir_acao'
    assert hasattr(agente, "decidir_acao")
