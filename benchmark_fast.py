# ==============================
# benchmark_fast.py (revisado e robusto)
# ==============================
'''
Este benchmark executa múltiplas simulações dos agentes 'lógico' e 'genético'
no ambiente Wumpus World, para diferentes tamanhos de mundo (4x4, 6x6, 8x8).
Para cada combinação agente+tamanho, executa várias rodadas em paralelo,
mede o tempo de execução, salva os resultados e gráficos em pastas organizadas,
e exibe um resumo com as taxas de vitória, morte, sobrevivência e tempos médios.
'''

import time
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from joblib import Parallel, delayed
from world.world import World
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent
import os
from datetime import datetime
import seaborn as sns

# Dicionário que associa nomes de agentes às suas classes
AGENTES_DISPONIVEIS = {
    'logico': LogicAgent,
    'genetico': GeneticAgent
}

TEMPOS_MEDIOS_ESTIMADOS = {
    'logico': 0.10,
    'genetico': 0.30
}

def simular_execucao(agente_cls, world_size, seed, parametros=None):
    mundo = World(size=world_size, seed=seed)
    agente = agente_cls(mundo, **(parametros or {}))
    if hasattr(agente, "logger"):
        agente.logger = None

    try:
        inicio = time.perf_counter()
        resultado = agente.run()
        fim = time.perf_counter()
    except Exception as e:
        print(f"❌ Erro durante execução com semente {seed}: {e}")
        return None  # falha na execução

    tempo = fim - inicio

    if mundo.won:
        status = "vitória"
    elif not mundo.is_alive:
        status = "morte"
    else:
        status = "sobreviveu"

    # Garante retorno consistente com dados extras
    # O GeneticAgent devolve os dados extras em "dados_extra" (antes lia "fitness", sempre vazio: #24)
    dados_extra = resultado.get("dados_extra", {}) if isinstance(resultado, dict) else {}

    return {
        "status": status,
        "tempo": tempo,
        "dados_extra": dados_extra
    }

def executar_benchmark(agente_nome, world_size, num_execucoes, parametros_agentes=None):
    agente_cls = AGENTES_DISPONIVEIS[agente_nome]

    print(f"\n🔁 Iniciando: agente = '{agente_nome}', mundo = {world_size}x{world_size}")
    estimativa = TEMPOS_MEDIOS_ESTIMADOS.get(agente_nome, 0.2) * num_execucoes
    print(f"⏳ Estimativa de tempo total: {estimativa:.2f}s")

    resultados = Parallel(n_jobs=-1)(
        delayed(simular_execucao)(agente_cls, world_size, seed, (parametros_agentes or {}).get(agente_nome, {}))
        for seed in range(num_execucoes)
    )

    # Filtra apenas execuções válidas
    resultados_validos = [r for r in resultados if r is not None]

    vitorias = sum(1 for r in resultados_validos if r["status"] == "vitória")
    mortes = sum(1 for r in resultados_validos if r["status"] == "morte")
    sobrevivencias = sum(1 for r in resultados_validos if r["status"] == "sobreviveu")
    tempos = [r["tempo"] for r in resultados_validos]
    tempo_total = sum(tempos)
    tempo_medio = tempo_total / len(tempos) if tempos else 0.0

    # Dados extras da primeira execução válida, no mesmo formato do benchmark.py
    # (gerar_graficos_avancados espera os dados de uma execução, não uma lista de execuções)
    dados_extra = next((r["dados_extra"] for r in resultados_validos if r["dados_extra"]), {})

    return {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        "vitórias": vitorias,
        "mortes": mortes,
        "sobreviveu": sobrevivencias,
        "tempo_total": tempo_total,
        "tempo_médio": tempo_medio,
        "dados_extra": dados_extra
    }

def gerar_graficos(df_resultados, output_dir):
    """
    Gera e salva gráficos simples de barras para vitórias, mortes e tempo médio por agente e tamanho de mundo.
    """
    # Gráfico de vitórias por agente e tamanho de mundo
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_resultados, x="tamanho_mundo", y="vitórias", hue="agente")
    plt.title("Vitórias por agente e tamanho de mundo")
    plt.savefig(os.path.join(output_dir, "vitorias.png"))
    plt.close()

    # Gráfico de mortes por agente e tamanho de mundo
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_resultados, x="tamanho_mundo", y="mortes", hue="agente")
    plt.title("Mortes por agente e tamanho de mundo")
    plt.savefig(os.path.join(output_dir, "mortes.png"))
    plt.close()

    # Gráfico de tempo médio por agente e tamanho de mundo
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_resultados, x="tamanho_mundo", y="tempo_médio", hue="agente")
    plt.title("Tempo médio por execução")
    plt.savefig(os.path.join(output_dir, "tempo_medio.png"))
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execucoes", type=int, default=10)
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument("--agentes", nargs="+", choices=AGENTES_DISPONIVEIS.keys(),
                        default=list(AGENTES_DISPONIVEIS.keys()))
    args = parser.parse_args()

    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(logs_dir, f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    resultados = []
    for size in args.sizes:
        for nome in args.agentes:
            resultado = executar_benchmark(nome, size, args.execucoes)
            resultados.append(resultado)

    df_resultados = pd.DataFrame(resultados)
    csv_path = os.path.join(output_dir, "resultados_benchmark.csv")
    df_resultados.to_csv(csv_path, index=False)
    gerar_graficos(df_resultados, output_dir)
    print(f"\n📊 Resultados salvos em '{csv_path}'")
    print(f"📈 Gráficos salvos em '{output_dir}'")

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
        print(f"⏱️ Tempo médio por execução: {tempo_medio:.3f} segundos")