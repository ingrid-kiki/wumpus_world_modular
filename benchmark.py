# ==============================
# benchmark.py
# ==============================
'''
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, usando um mundo de tamanho 4x4.
Para cada agente, executa várias rodadas, mede o tempo de execução,
e retorna um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
'''

import time
from world.world import World
from agents.manual_agent import ManualAgent
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
    'manual': ManualAgent,
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

TEMPOS_MEDIOS_ESTIMADOS = {
    'logico': 0.10,
    'genetico': 0.30
}

def executar_benchmark(agente_nome, world_size=4, num_execucoes=10):
    vitorias, mortes, sobrevivencias = 0, 0, 0
    dados_extra_capturados = {}
    tempos = []
    tempo_estimado = TEMPOS_MEDIOS_ESTIMADOS.get(agente_nome, 0.2) * num_execucoes
    print(f"\n⏳ Estimativa de tempo total para '{agente_nome}' ({world_size}x{world_size}): {tempo_estimado:.2f}s")

    for i in range(num_execucoes):
        seed = i
        mundo = World(size=world_size, seed=seed)
        agente_cls = AGENTES_DISPONIVEIS[agente_nome]
        agente = agente_cls(mundo)
        if hasattr(agente, "logger"):
            agente.logger = None

        print(f"🚀 Execução {i + 1}/{num_execucoes} [{agente_nome}]")

        inicio = time.perf_counter()
        try:
            resultado = agente.run()
        except Exception as e:
            print(f"❌ Erro na execução {i + 1}: {e}")
            resultado = None
        fim = time.perf_counter()

        tempos.append(fim - inicio)

        if i == 0 and agente_nome == "genetico" and isinstance(resultado, dict):
            dados_extra_capturados = resultado.get("dados_extra", {})
        
        if mundo.won:
            vitorias += 1
        elif not mundo.is_alive:
            mortes += 1
        else:
            sobrevivencias += 1

    tempo_total = sum(tempos)
    tempo_medio = tempo_total / num_execucoes

    retorno = {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        "vitórias": vitorias,
        "mortes": mortes,
        "sobreviveu": sobrevivencias,
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio,
        "dados_extra": dados_extra_capturados
    }

    return retorno

if __name__ == "__main__":
    for nome in AGENTES_DISPONIVEIS.keys():
        resultado = executar_benchmark(nome, world_size=4, num_execucoes=3)
        print(f"\nResumo para {nome}:")
        print(f"Vitórias: {resultado['vitórias']}")
        print(f"Mortes: {resultado['mortes']}")
        print(f"Sobreviveu sem vencer: {resultado['sobreviveu']}")
        print(f"Tempo total: {resultado['tempo_total']:.2f}s")
        print(f"Tempo médio por execução: {resultado['tempo_médio']:.3f}s")