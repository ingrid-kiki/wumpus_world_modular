# ==============================
# benchmark_graficos.py
# ==============================
"""
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, para diferentes tamanhos de mundo (4x4, 6x6, 8x8).
Para cada combinação agente+tamanho, executa várias rodadas,
mede o tempo de execução, salva os resultados em CSV e gera gráficos comparativos,
exibindo um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
"""

import argparse
import os
from datetime import datetime

import matplotlib

from utils.execucao import contar, executar_uma

matplotlib.use("Agg")  # só salva arquivos, nunca abre janela (evita depender do Tk)
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd

from agents.genetic_agent import GeneticAgent
from agents.logic_agent import LogicAgent
from agents.random_search_agent import RandomSearchAgent
from world.world import World

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {"logico": LogicAgent, "genetico": GeneticAgent, "aleatorio": RandomSearchAgent}


def executar_benchmark(agente_nome, world_size, num_execucoes, parametros_agentes=None):
    # Status de cada execução: "vitória", "morte", "sobreviveu" ou "erro" (#30)
    status = []
    tempos = []  # Lista para armazenar o tempo de cada execução
    dados_extra_capturados = {}  # Dados extras da primeira execução (agente genético)

    # Executa o benchmark várias vezes, mudando a semente para cada rodada
    for i in range(num_execucoes):
        seed = i  # muda a semente em cada rodada para garantir variedade
        mundo = World(size=world_size, seed=seed)  # Cria o mundo com a semente atual
        agente = AGENTES_DISPONIVEIS[agente_nome](
            mundo, **(parametros_agentes or {}).get(agente_nome, {})
        )  # Instancia o agente escolhido
        agente.logger = None  # desativa logging

        # Executa o agente; um erro não derruba o benchmark nem vira resultado (#30)
        execucao = executar_uma(
            agente, mundo, rotulo=f"{i + 1}/{num_execucoes} [{agente_nome} - {world_size}x{world_size}]"
        )
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

    # Retorna um dicionário com os resultados para posterior análise
    return {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        "vitórias": vitorias,
        "mortes": mortes,
        "sobreviveu": sobrevivencias,
        "erros": contagem["erros"],
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio,
        "dados_extra": dados_extra_capturados,
    }


def gerar_graficos(df, output_dir="."):
    # Gera gráficos de barras para vitórias, mortes e sobrevivências
    for metric in ["vitórias", "mortes", "sobreviveu"]:
        plt.figure(figsize=(8, 5))
        for tamanho in sorted(df["tamanho_mundo"].unique()):
            subset = df[df["tamanho_mundo"] == tamanho]
            plt.bar(
                [f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
                subset[metric],
                label=f"{tamanho}x{tamanho}",
            )
        plt.title(f"Comparação de {metric.capitalize()} por agente e tamanho do mundo")
        plt.ylabel("Quantidade")
        plt.xlabel("Agente-Tamanho")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"grafico_{metric}.png"))
        plt.close()

    # Gera gráfico de barras para o tempo médio de execução
    plt.figure(figsize=(8, 5))
    for tamanho in sorted(df["tamanho_mundo"].unique()):
        subset = df[df["tamanho_mundo"] == tamanho]
        plt.bar(
            [f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
            subset["tempo_médio"],
            label=f"{tamanho}x{tamanho}",
        )
    plt.title("Tempo médio de execução por agente e tamanho do mundo")
    plt.ylabel("Tempo médio (s)")
    plt.xlabel("Agente-Tamanho")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_tempo_medio.png"))
    plt.close()


if __name__ == "__main__":
    # Parser de argumentos para personalizar execuções via terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("--execucoes", type=int, default=10)
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument(
        "--agentes", nargs="+", choices=AGENTES_DISPONIVEIS.keys(), default=list(AGENTES_DISPONIVEIS.keys())
    )
    parser.add_argument("--saida", type=str, default=None, help="Pasta de saída (padrão: logs/run_AAAAMMDD_HHMMSS)")
    args = parser.parse_args()

    # Grava na pasta do run, como os outros benchmarks (antes gravava na pasta atual)
    output_dir = args.saida or os.path.join("logs", datetime.now().strftime("run_%Y%m%d_%H%M%S"))
    os.makedirs(output_dir, exist_ok=True)

    # Executa o benchmark para cada combinação de tamanho de mundo e agente selecionado
    resultados = []
    for size in args.sizes:
        for nome in args.agentes:
            resultado = executar_benchmark(nome, size, args.execucoes)
            resultados.append(resultado)

    # Salva os resultados em um DataFrame do pandas
    df_resultados = pd.DataFrame([{k: v for k, v in r.items() if k != "dados_extra"} for r in resultados])
    csv_path = os.path.join(output_dir, "resultados_benchmark.csv")
    df_resultados.to_csv(csv_path, index=False)  # Exporta para CSV, só com colunas escalares
    gerar_graficos(df_resultados, output_dir)  # Gera e salva os gráficos
    print(f"\n📊 Resultados salvos em '{csv_path}'")
    print(f"📈 Gráficos salvos em '{output_dir}'")

    # Exibe o resumo dos resultados do benchmark para cada agente e tamanho de mundo
    for _, row in df_resultados.iterrows():
        agente_nome = row["agente"]
        tamanho = row["tamanho_mundo"]
        vitorias = row["vitórias"]
        mortes = row["mortes"]
        sobrevivencias = row["sobreviveu"]
        tempo_total = row["tempo_total"]
        tempo_medio = row["tempo_médio"]
        erros = row["erros"]
        num_execucoes = vitorias + mortes + sobrevivencias + erros

        print(f"\n📊 RESULTADOS - Agente: {agente_nome.upper()} | Tamanho: {tamanho}x{tamanho}")
        print(f"🏆 Vitórias: {vitorias} ({(vitorias / num_execucoes) * 100:.1f}%)")
        print(f"☠️ Mortes: {mortes} ({(mortes / num_execucoes) * 100:.1f}%)")
        print(f"🤔 Sobreviveu sem vencer: {sobrevivencias} ({(sobrevivencias / num_execucoes) * 100:.1f}%)")
        if erros:
            print(f"❌ Erros: {erros}")
        print(f"⏱️ Tempo total: {tempo_total:.2f} segundos")
        print(f"⏱️ Tempo médio por execução: {tempo_medio:.2f} segundos")
