# ==============================
# benchmark_graficos.py
# ==============================
'''
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, para diferentes tamanhos de mundo (4x4, 6x6, 8x8).
Para cada combinação agente+tamanho, executa várias rodadas,
mede o tempo de execução, salva os resultados em CSV e gera gráficos comparativos,
exibindo um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
'''

import time
import argparse
import matplotlib
matplotlib.use("Agg")  # só salva arquivos, nunca abre janela (evita depender do Tk)
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd
from world.world import World
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

def executar_benchmark(agente_nome, world_size, num_execucoes, parametros_agentes=None):
    # Inicializa contadores de vitórias, mortes e sobrevivências
    vitorias, mortes, sobrevivencias = 0, 0, 0
    tempos = []  # Lista para armazenar o tempo de cada execução
    dados_extra_capturados = {}  # Dados extras da primeira execução (agente genético)

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(num_execucoes):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=world_size, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES_DISPONIVEIS[agente_nome](mundo, **(parametros_agentes or {}).get(agente_nome, {}))  # Instancia o agente escolhido
        agente.logger = None  # desativa logging

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

    # Retorna um dicionário com os resultados para posterior análise
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

    # Exibe o resumo dos resultados do benchmark para cada agente e tamanho de mundo
    for _, row in df_resultados.iterrows():
        agente_nome = row['agente']
        tamanho = row['tamanho_mundo']
        vitorias = row['vitórias']
        mortes = row['mortes']
        sobrevivencias = row['sobreviveu']
        tempo_total = row['tempo_total']
        tempo_medio = row['tempo_médio']
        num_execucoes = vitorias + mortes + sobrevivencias

        print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()} | Tamanho: {tamanho}x{tamanho}")
        print(f"🏆 Vitórias: {vitorias} ({(vitorias/num_execucoes)*100:.1f}%)")
        print(f"☠️ Mortes: {mortes} ({(mortes/num_execucoes)*100:.1f}%)")
        print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias/num_execucoes)*100:.1f}%)")
        print(f"⏱️ Tempo total: {tempo_total:.2f} segundos")
        print(f"⏱️ Tempo médio por execução: {tempo_medio:.2f} segundos")