import time
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from joblib import Parallel, delayed
from world.world import World
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

def simular_execucao(agente_cls, world_size, seed):
    # Cria uma instância do mundo com a semente fornecida
    mundo = World(size=world_size, seed=seed)
    # Cria o agente correspondente
    agente = agente_cls(mundo)
    agente.logger = None  # Desativa logging para não poluir a saída

    # Marca o tempo de início da execução
    inicio = time.perf_counter()
    agente.run()  # Executa o agente no mundo
    fim = time.perf_counter()  # Marca o tempo de fim da execução
    tempo = fim - inicio  # Calcula o tempo gasto

    # Determina o status final do agente
    if mundo.won:
        status = "vitória"
    elif not mundo.is_alive:
        status = "morte"
    else:
        status = "sobreviveu"
    return status, tempo

def executar_benchmark(agente_nome, world_size, num_execucoes):
    # Obtém a classe do agente a partir do nome
    agente_cls = AGENTES_DISPONIVEIS[agente_nome]

    # Executa as simulações em paralelo usando joblib
    resultados = Parallel(n_jobs=-1)(
        delayed(simular_execucao)(agente_cls, world_size, i)
        for i in range(num_execucoes)
    )

    # Conta os resultados de cada tipo
    vitorias = sum(1 for r, _ in resultados if r == "vitória")
    mortes = sum(1 for r, _ in resultados if r == "morte")
    sobrevivencias = sum(1 for r, _ in resultados if r == "sobreviveu")
    tempos = [t for _, t in resultados]
    tempo_total = sum(tempos)
    tempo_medio = tempo_total / num_execucoes

    # Retorna um dicionário com os resultados para posterior análise
    return {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        "vitórias": vitorias,
        "mortes": mortes,
        "sobreviveu": sobrevivencias,
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio
    }

def gerar_graficos(df):
    # Gera gráficos de barras para vitórias, mortes e sobrevivências
    for metric in ["vitórias", "mortes", "sobreviveu"]:
        plt.figure(figsize=(8, 5))
        for tamanho in sorted(df["tamanho_mundo"].unique()):
            subset = df[df["tamanho_mundo"] == tamanho]
            plt.bar([f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
                    subset[metric], label=f"{tamanho}x{tamanho}")
        plt.title(f"Comparação de {metric.capitalize()} por agente e tamanho do mundo")
        plt.ylabel("Quantidade")
        plt.xlabel("Agente-Tamanho")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"grafico_{metric}.png")

    # Gera gráfico de barras para o tempo médio de execução
    plt.figure(figsize=(8, 5))
    for tamanho in sorted(df["tamanho_mundo"].unique()):
        subset = df[df["tamanho_mundo"] == tamanho]
        plt.bar([f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
                subset["tempo_médio"], label=f"{tamanho}x{tamanho}")
    plt.title("Tempo médio de execução por agente e tamanho do mundo")
    plt.ylabel("Tempo médio (s)")
    plt.xlabel("Agente-Tamanho")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("grafico_tempo_medio.png")

if __name__ == "__main__":
    # Parser de argumentos para personalizar execuções via terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("--execucoes", type=int, default=10)
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument("--agentes", nargs="+", choices=AGENTES_DISPONIVEIS.keys(),
                        default=list(AGENTES_DISPONIVEIS.keys()))
    args = parser.parse_args()

    # Executa o benchmark para cada combinação de tamanho de mundo e agente selecionado
    resultados = []
    for size in args.sizes:
        for nome in args.agentes:
            resultado = executar_benchmark(nome, size, args.execucoes)
            resultados.append(resultado)

    # Salva os resultados em um DataFrame do pandas
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv("resultados_benchmark.csv", index=False)  # Exporta para CSV
    gerar_graficos(df_resultados)  # Gera e salva os gráficos
    print("\n📊 Resultados salvos em 'resultados_benchmark.csv'")
    print("📈 Gráficos salvos como 'grafico_*.png'")