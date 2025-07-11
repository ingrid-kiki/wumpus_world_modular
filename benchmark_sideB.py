# ==============================
# benchmark_sideB.py
# ==============================
import time
from world.world import World
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES = {
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

NUM_EXECUCOES = 10  # Número de execuções para cada combinação agente + tamanho
WORLD_SIZES = [4, 6, 8]  # Tamanhos de mundo a serem testados

# Tempos médios estimados para cada agente (usado apenas para exibir estimativa)
TEMPOS_MEDIOS_ESTIMADOS = {
    'logico': 0.10,
    'genetico': 0.30
}

def executar_benchmark(agente_nome, world_size):
    # Inicializa contadores de vitórias, mortes e sobrevivências
    vitorias, mortes, sobrevivencias = 0, 0, 0
    tempos = []  # Lista para armazenar o tempo de cada execução

    # Calcula e exibe a estimativa de tempo total para o benchmark
    tempo_estimado = TEMPOS_MEDIOS_ESTIMADOS.get(agente_nome, 0.2) * NUM_EXECUCOES
    print(f"\n🔁 Iniciando: agente = '{agente_nome}', mundo = {world_size}x{world_size}")
    print(f"⏳ Estimativa de tempo total: {tempo_estimado:.2f} segundos")

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(NUM_EXECUCOES):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=world_size, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES[agente_nome](mundo)       # Instancia o agente escolhido
        agente.logger = None  # desativa logging para não poluir a saída

        # Exibe informações da execução atual
        print(f"🚀 Execução {i+1}/{NUM_EXECUCOES} [{agente_nome} - {world_size}x{world_size}]")

        # Marca o tempo de início da execução
        inicio = time.perf_counter()
        agente.run()  # Executa o agente no mundo
        fim = time.perf_counter()  # Marca o tempo de fim da execução

        # Salva o tempo gasto nesta execução
        tempos.append(fim - inicio)

        # Atualiza os contadores de acordo com o resultado da execução
        if mundo.won:
            vitorias += 1
        elif not mundo.is_alive:
            mortes += 1
        else:
            sobrevivencias += 1

    # Calcula o tempo total e o tempo médio por execução
    tempo_total = sum(tempos)
    tempo_medio = tempo_total / NUM_EXECUCOES

    # Exibe o resumo dos resultados do benchmark para o agente e tamanho de mundo
    print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()} | Mundo: {world_size}x{world_size}")
    print(f"🏆 Vitórias: {vitorias} ({(vitorias/NUM_EXECUCOES)*100:.1f}%)")
    print(f"☠️ Mortes: {mortes} ({(mortes/NUM_EXECUCOES)*100:.1f}%)")
    print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias/NUM_EXECUCOES)*100:.1f}%)")
    print(f"⏱️ Tempo total real: {tempo_total:.2f} segundos")
    print(f"⏱️ Tempo médio por execução: {tempo_medio:.3f} segundos\n")

if __name__ == "__main__":
    # Executa o benchmark para cada combinação de tamanho de mundo e agente selecionado
    for size in WORLD_SIZES:
        for nome in AGENTES.keys():
            executar_benchmark(nome, size)