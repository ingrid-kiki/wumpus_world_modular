# ==============================
# benchmark.py
# ==============================
import time
from world.world import World
from agents.manual_agent import ManualAgent  # Só para referência, não usado aqui
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES = {
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

NUM_EXECUCOES = 20   # Número de execuções para cada agente no benchmark
WORLD_SIZE = 4       # Tamanho do mundo (4x4)

def executar_benchmark(agente_nome):
    # Inicializa contadores de vitórias, mortes e sobrevivências
    vitorias, mortes, sobrevivencias = 0, 0, 0
    tempos = []

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(NUM_EXECUCOES):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=WORLD_SIZE, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES[agente_nome](mundo)       # Instancia o agente escolhido
        agente.logger = None  # desativa logging para não poluir a saída

        print(f"🚀 Execução {i+1}/{NUM_EXECUCOES} [{agente_nome}]")
        
        inicio = time.perf_counter()
        agente.run()  # Executa o agente no mundo
        fim = time.perf_counter()
        
        tempos.append(fim - inicio)

        # Atualiza os contadores de acordo com o resultado da execução
        if mundo.won:
            vitorias += 1
        elif not mundo.is_alive:
            mortes += 1
        else:
            sobrevivencias += 1
    
    # Calcula o tempo médio de execução
    tempo_total = sum(tempos)
    tempo_medio = tempo_total / NUM_EXECUCOES

    # Exibe o resumo dos resultados do benchmark para o agente
    print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()}")
    print(f"🏆 Vitórias: {vitorias} ({(vitorias/NUM_EXECUCOES)*100:.1f}%)")
    print(f"☠️ Mortes: {mortes} ({(mortes/NUM_EXECUCOES)*100:.1f}%)")
    print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias/NUM_EXECUCOES)*100:.1f}%)\n")
    print(f"⏱️ Tempo total: {tempo_total:.2f} segundos")
    print(f"⏱️ Tempo médio por execução: {tempo_medio:.3f} segundos\n")

if __name__ == "__main__":
    # Executa o benchmark para cada agente definido em AGENTES
    for nome in AGENTES.keys():
        executar_benchmark(nome)
