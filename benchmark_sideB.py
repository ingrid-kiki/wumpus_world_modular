# ==============================
# benchmark_sideB.py
# ==============================
'''
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, para diferentes tamanhos de mundo (4x4, 6x6, 8x8).
Para cada combinação agente+tamanho, executa várias rodadas, mede o tempo de execução,
e exibe um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
'''

from utils.execucao import contar, executar_uma
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

def executar_benchmark(agente_nome, world_size, num_execucoes=NUM_EXECUCOES, parametros_agentes=None):
    # Status de cada execução: "vitória", "morte", "sobreviveu" ou "erro" (#30)
    status = []
    tempos = []  # Lista para armazenar o tempo de cada execução
    dados_extra_capturados = {}  # Dados extras da primeira execução (agente genético)

    print(f"\n🔁 Iniciando: agente = '{agente_nome}', mundo = {world_size}x{world_size}")

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(num_execucoes):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=world_size, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES_DISPONIVEIS[agente_nome](mundo, **(parametros_agentes or {}).get(agente_nome, {}))       # Instancia o agente escolhido
        agente.logger = None  # desativa logging para não poluir a saída

        # Exibe informações da execução atual
        print(f"🚀 Execução {i+1}/{num_execucoes} [{agente_nome} - {world_size}x{world_size}]")

        # Executa o agente; um erro não derruba o benchmark nem vira resultado (#30)
        execucao = executar_uma(agente, mundo, rotulo=f"{i+1}/{num_execucoes} [{agente_nome} - {world_size}x{world_size}]")
        tempos.append(execucao["tempo"])
        status.append(execucao["status"])

        # Dados extras da primeira execução que terminou sem erro
        if not dados_extra_capturados and isinstance(execucao["resultado"], dict):
            dados_extra_capturados = execucao["resultado"].get("dados_extra", {})

    # Conta vitórias, mortes, sobrevivências e erros
    contagem = contar(status)
    vitorias, mortes, sobrevivencias = contagem["vitórias"], contagem["mortes"], contagem["sobreviveu"]

    # Calcula o tempo total e o tempo médio por execução
    tempo_total = sum(tempos)
    tempo_medio = tempo_total / num_execucoes

    # Exibe o resumo dos resultados do benchmark para o agente e tamanho de mundo
    print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()} | Mundo: {world_size}x{world_size}")
    print(f"🏆 Vitórias: {vitorias} ({(vitorias/num_execucoes)*100:.1f}%)")
    print(f"☠️ Mortes: {mortes} ({(mortes/num_execucoes)*100:.1f}%)")
    print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias/num_execucoes)*100:.1f}%)")
    if contagem["erros"]:
        print(f"❌ Erros: {contagem['erros']}")
    print(f"⏱️ Tempo total real: {tempo_total:.2f} segundos")
    print(f"⏱️ Tempo médio por execução: {tempo_medio:.3f} segundos\n")

    # Mesmo formato do benchmark.py, para funcionar com main.py --benchmark (#24)
    return {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        "vitórias": vitorias,
        "mortes": mortes,
        "sobreviveu": sobrevivencias,
        "erros": contagem["erros"],
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio,
        "dados_extra": dados_extra_capturados
    }

if __name__ == "__main__":
    # Executa o benchmark para cada combinação de tamanho de mundo e agente selecionado
    for size in WORLD_SIZES:
        for nome in AGENTES_DISPONIVEIS.keys():
            executar_benchmark(nome, size)