# ==============================
# tests/test_execution_time.py
# ==============================
'''
# Este arquivo contém um teste unitário para medir o tempo de execução do agente genético (GeneticAgent)
# no ambiente Wumpus World. O objetivo é garantir que o agente executa dentro de um tempo razoável,
# ajudando a identificar possíveis problemas de desempenho ou loops infinitos.
#
# Explicação do teste:
# - Cria uma instância do mundo (World) com tamanho 4x4 e semente fixa para reprodutibilidade.
# - Cria uma instância do agente genético (GeneticAgent) passando o mundo criado.
# - Mede o tempo antes e depois de executar o método run() do agente.
# - Calcula a duração da execução.
# - Imprime o tempo de execução para análise didática.
# - Garante que o tempo de execução está abaixo de um limite (ex: 10 segundos).
#   Esse limite pode ser ajustado conforme a complexidade do agente e do ambiente.
#
# Esse teste é útil para monitorar a performance dos agentes durante o desenvolvimento.
'''

import os
import pytest
import time
from agents.genetic_agent import GeneticAgent
from world.world import World

# Obtém o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Cria o diretório de saída para os logs, com um timestamp único
output_dir = os.path.join(BASE_DIR, "logs", f"run_{int(time.time())}")

def test_execution_time():
    # Cria o mundo e o agente genético
    world = World(size=4, seed=42)
    agent = GeneticAgent(world)
    # Marca o tempo inicial
    start = time.time()
    # Executa o agente
    agent.run()
    # Marca o tempo final
    end = time.time()

    # Calcula a duração da execução
    duration = end - start
    # Imprime o tempo de execução para análise didática
    print(f"⏱️ Tempo de execução: {duration:.2f}s")
    # Garante que o tempo de execução está dentro do limite esperado
    assert duration < 10  # ajuste conforme necessário
