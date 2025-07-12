# ==============================
# benchmark_custom.py
# ==============================
'''
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, para diferentes tamanhos de mundo (4x4, 6x6, 8x8).
Para cada combinação agente+tamanho, executa várias rodadas, mede o tempo de execução,
e exibe um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
Permite customizar agentes, tamanhos e número de execuções via argumentos de linha de comando.
'''

import time
import argparse
from world.world import World
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

# Tempos médios estimados para cada agente (usado apenas para exibir estimativa)
TEMPOS_MEDIOS_ESTIMADOS = {
    'logico': 0.10,
    'genetico': 0.30
}

def executar_benchmark(agente_nome, world_size, num_execucoes, silent=False):
    # Inicializa contadores de vitórias, mortes e sobrevivências
    vitorias, mortes, sobrevivencias = 0, 0, 0
    tempos = []  # Lista para armazenar o tempo de cada execução

    # Calcula e exibe a estimativa de tempo total para o benchmark
    tempo_estimado = TEMPOS_MEDIOS_ESTIMADOS.get(agente_nome, 0.2) * num_execucoes
    print(f"\n🔁 Iniciando: agente = '{agente_nome}', mundo = {world_size}x{world_size}")
    print(f"⏳ Estimativa de tempo total: {tempo_estimado:.2f} segundos")

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(num_execucoes):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=world_size, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES_DISPONIVEIS[agente_nome](mundo)  # Instancia o agente escolhido
        agente.logger = None  # desativa logging para não poluir a saída

        # Exibe informações da execução atual (se não estiver em modo silencioso)
        if not silent:
            print(f"🚀 Execução {i+1}/{num_execucoes} [{agente_nome} - {world_size}x{world_size}]")

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
    tempo_medio = tempo_total / num_execucoes

    # Exibe o resumo dos resultados do benchmark para o agente e tamanho de mundo
    print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()} | Mundo: {world_size}x{world_size}")
    print(f"🏆 Vitórias: {vitorias} ({(vitorias/num_execucoes)*100:.1f}%)")
    print(f"☠️ Mortes: {mortes} ({(mortes/num_execucoes)*100:.1f}%)")
    print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias/num_execucoes)*100:.1f}%)")
    print(f"⏱️ Tempo total real: {tempo_total:.2f} segundos")
    print(f"⏱️ Tempo médio por execução: {tempo_medio:.3f} segundos\n")

if __name__ == "__main__":
    # Cria o parser de argumentos para execução via terminal
    parser = argparse.ArgumentParser(description="Benchmark dos agentes no mundo de Wumpus")
    parser.add_argument("--execucoes", type=int, default=10, help="Número de execuções por agente/tamanho")
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8], help="Tamanhos do mundo (ex: 4 6 8)")
    parser.add_argument("--agentes", nargs="+", choices=AGENTES_DISPONIVEIS.keys(), default=list(AGENTES_DISPONIVEIS.keys()), help="Agentes a testar")
    parser.add_argument("--silent", action="store_true", help="Modo silencioso (menos prints)")
    args = parser.parse_args()

    # Executa o benchmark para cada combinação de tamanho de mundo e agente selecionado
    for size in args.sizes:
        for nome in args.agentes:
            executar_benchmark(nome, size, args.execucoes, silent=args.silent)