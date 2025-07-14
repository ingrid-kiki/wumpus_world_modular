# ==============================
# tests/test_fitness_history.py
# ==============================
'''
# Este arquivo contém um teste unitário para verificar o rastreamento do histórico de fitness
# do agente genético (GeneticAgent) durante a execução do algoritmo genético no ambiente Wumpus World.
#
# O objetivo é garantir que o agente armazena corretamente a evolução do fitness ao longo das gerações,
# permitindo a análise e visualização do desempenho do algoritmo.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (GeneticAgent) com parâmetros customizados.
# - Executa o agente e obtém o resultado da simulação, incluindo o histórico de fitness.
# - Salva o histórico de fitness em um arquivo CSV temporário para facilitar a geração de gráficos.
# - Garante que o histórico de fitness não está vazio (ou seja, o rastreamento foi realizado).
'''

import os
import pytest
from agents.genetic_agent import GeneticAgent
from world.world import World

def test_fitness_history_tracking(tmp_path):
    # Cria o mundo e o agente genético com parâmetros customizados
    world = World(size=4, seed=42)
    agent = GeneticAgent(world, population_size=30, gens=20, chrom_length=10)
    # Executa o agente e obtém o resultado
    result = agent.run()
    fitness = result["fitness"]
    
    # Salva o histórico de fitness em um arquivo CSV temporário
    import datetime
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(BASE_DIR, "logs", f"run_{timestamp}")
    output_file = tmp_path / "fitness_history.csv"
    with open(output_file, "w") as f:
        for f_val in fitness:
            f.write(f"{f_val}\n")

    # Garante que o histórico de fitness não está vazio
    assert len(fitness) > 0
