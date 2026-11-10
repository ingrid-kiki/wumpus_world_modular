# ==============================
# benchmark.py
# ==============================
"""
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, usando um mundo de tamanho 4x4.
Para cada agente, executa várias rodadas, mede o tempo de execução,
e retorna um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
"""

from agents.genetic_agent import GeneticAgent
from agents.logic_agent import LogicAgent
from agents.manual_agent import ManualAgent
from agents.random_search_agent import RandomSearchAgent
from utils.execucao import contar, executar_uma
from world.world import World

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
    "manual": ManualAgent,
    "logico": LogicAgent,
    "genetico": GeneticAgent,
    "aleatorio": RandomSearchAgent,
}


def executar_benchmark(agente_nome, world_size=4, num_execucoes=10, parametros_agentes=None):
    status = []  # "vitória", "morte", "sobreviveu" ou "erro", uma por execução (#30)
    dados_extra_capturados = {}
    tempos = []

    for i in range(num_execucoes):
        seed = i
        mundo = World(size=world_size, seed=seed)
        agente_cls = AGENTES_DISPONIVEIS[agente_nome]
        agente = agente_cls(mundo, **(parametros_agentes or {}).get(agente_nome, {}))
        if hasattr(agente, "logger"):
            agente.logger = None

        print(f"🚀 Execução {i + 1}/{num_execucoes} [{agente_nome}]")

        execucao = executar_uma(agente, mundo, rotulo=f"{i + 1}/{num_execucoes} [{agente_nome}]")
        tempos.append(execucao["tempo"])
        status.append(execucao["status"])

        # Dados extras da primeira execução que terminou sem erro
        if not dados_extra_capturados and isinstance(execucao["resultado"], dict):
            dados_extra_capturados = execucao["resultado"].get("dados_extra", {})

    tempo_total = sum(tempos)
    tempo_medio = tempo_total / num_execucoes

    retorno = {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        **contar(status),
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio,
        "dados_extra": dados_extra_capturados,
    }

    return retorno


if __name__ == "__main__":
    # Só agentes automáticos: o manual pede ações pelo teclado e não faz sentido num benchmark (#30)
    for nome in [n for n in AGENTES_DISPONIVEIS if n != "manual"]:
        resultado = executar_benchmark(nome, world_size=4, num_execucoes=3)
        print(f"\nResumo para {nome}:")
        print(f"Vitórias: {resultado['vitórias']}")
        print(f"Mortes: {resultado['mortes']}")
        print(f"Sobreviveu sem vencer: {resultado['sobreviveu']}")
        print(f"Erros: {resultado['erros']}")
        print(f"Tempo total: {resultado['tempo_total']:.2f}s")
        print(f"Tempo médio por execução: {resultado['tempo_médio']:.3f}s")
