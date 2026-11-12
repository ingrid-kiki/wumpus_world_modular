# ==============================
# tests/test_fitness_history.py
# ==============================
"""
# Este arquivo contém um teste unitário para verificar o rastreamento do histórico de fitness
# do agente genético (AgenteGenetico) durante a execução do algoritmo genético no ambiente Wumpus World.
#
# O objetivo é garantir que o agente armazena corretamente a evolução do fitness ao longo das gerações,
# permitindo a análise e visualização do desempenho do algoritmo.
#
# Explicação do teste:
# - Cria uma instância do mundo (Mundo) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (AgenteGenetico) com parâmetros customizados.
# - Executa o agente e obtém o resultado da simulação, incluindo o histórico de fitness.
# - Salva o histórico de fitness em um arquivo CSV temporário para facilitar a geração de gráficos.
# - Garante que o histórico de fitness não está vazio (ou seja, o rastreamento foi realizado).
"""

from agents.genetic_agent import AgenteGenetico
from tests.conftest import GA_RAPIDO
from world.world import Mundo


def test_historico_de_fitness_registrado(tmp_path):
    # Cria o mundo e o agente genético com parâmetros customizados
    mundo = Mundo(tamanho=4, semente=42)
    agente = AgenteGenetico(mundo, **GA_RAPIDO)
    # Executa o agente e obtém o resultado
    result = agente.executar()
    fitness = result["dados_extra"]["fitness"]

    # Salva o histórico de fitness em um arquivo CSV temporário
    output_file = tmp_path / "historico_fitness.csv"
    with open(output_file, "w") as f:
        for f_val in fitness:
            f.write(f"{f_val}\n")

    # Garante que o histórico de fitness não está vazio
    assert len(fitness) > 0
