# ==============================
# benchmark_sideB.py
# ==============================
'''
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, para diferentes tamanhos de mundo (4x4, 6x6, 8x8).
Para cada combinação agente+tamanho, executa várias rodadas, mede o tempo de execução,
e exibe um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
'''

import time
from world.world import World
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
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

def executar_benchmark(agente_nome, world_size, num_execucoes=NUM_EXECUCOES, parametros_agentes=None):
    # Inicializa contadores de vitórias, mortes e sobrevivências
    vitorias, mortes, sobrevivencias = 0, 0, 0
    tempos = []  # Lista para armazenar o tempo de cada execução
    dados_extra_capturados = {}  # Dados extras da primeira execução (agente genético)

    # Calcula e exibe a estimativa de tempo total para o benchmark
    tempo_estimado = TEMPOS_MEDIOS_ESTIMADOS.get(agente_nome, 0.2) * num_execucoes
    print(f"\n🔁 Iniciando: agente = '{agente_nome}', mundo = {world_size}x{world_size}")
    print(f"⏳ Estimativa de tempo total: {tempo_estimado:.2f} segundos")

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(num_execucoes):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=world_size, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES_DISPONIVEIS[agente_nome](mundo, **(parametros_agentes or {}).get(agente_nome, {}))       # Instancia o agente escolhido
        agente.logger = None  # desativa logging para não poluir a saída

        # Exibe informações da execução atual
        print(f"🚀 Execução {i+1}/{num_execucoes} [{agente_nome} - {world_size}x{world_size}]")

        # Marca o tempo de início da execução
        inicio = time.perf_counter()
        resultado = agente.run()  # Executa o agente no mundo
        fim = time.perf_counter()  # Marca o tempo de fim da execução
        if i == 0 and isinstance(resultado, dict):
            dados_extra_capturados = resultado.get("dados_extra", {})

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
    tempo_medio = tempo_total / num_execucoes

    # Exibe o resumo dos resultados do benchmark para o agente e tamanho de mundo
    print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()} | Mundo: {world_size}x{world_size}")
    print(f"🏆 Vitórias: {vitorias} ({(vitorias/num_execucoes)*100:.1f}%)")
    print(f"☠️ Mortes: {mortes} ({(mortes/num_execucoes)*100:.1f}%)")
    print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias/num_execucoes)*100:.1f}%)")
    print(f"⏱️ Tempo total real: {tempo_total:.2f} segundos")
    print(f"⏱️ Tempo médio por execução: {tempo_medio:.3f} segundos\n")

    # Mesmo formato do benchmark.py, para funcionar com main.py --benchmark (#24)
    return {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        "vitórias": vitorias,
        "mortes": mortes,
        "sobreviveu": sobrevivencias,
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio,
        "dados_extra": dados_extra_capturados
    }

if __name__ == "__main__":
    # Executa o benchmark para cada combinação de tamanho de mundo e agente selecionado
    for size in WORLD_SIZES:
        for nome in AGENTES_DISPONIVEIS.keys():
            executar_benchmark(nome, size)