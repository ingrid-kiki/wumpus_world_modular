# ==============================
# main.py (revisado para menu interativo)
# ==============================

import argparse
import os
import sys
from datetime import datetime
import pandas as pd
import shlex
import importlib.util

from world.world import World
from agents.manual_agent import ManualAgent
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent
from utils.logger import Logger
from utils.graficos import gerar_graficos, gerar_graficos_avancados
from benchmark import executar_benchmark

# Dicionário de agentes disponíveis
AGENTES_DISPONIVEIS = {
    "manual": ManualAgent,
    "logico": LogicAgent,
    "genetico": GeneticAgent
}

def menu_interativo():
    print("=== Wumpus World ===")
    print("Escolha o modo de execução:")
    print("1 - Benchmark (vários agentes e tamanhos)")
    print("2 - Agente Manual (interativo)")
    print("3 - Agente Lógico (uma execução)")
    print("4 - Agente Genético (uma execução)")
    print("5 - Customizado via linha de comando (CLI)")
    escolha = input("Digite o número da opção desejada: ").strip()
    return escolha

def execucao_unica(agente_nome):
    size = int(input("Tamanho do mundo (ex: 4): ").strip())
    seed = input("Semente aleatória (opcional, pressione Enter para aleatório): ").strip()
    seed = int(seed) if seed else None

    mundo = World(size=size, seed=seed)
    agente_cls = AGENTES_DISPONIVEIS[agente_nome]
    agente = agente_cls(mundo)
    if hasattr(agente, "logger"):
        agente.logger = None  # Desativa logger para execução única

    print(f"\nExecutando agente '{agente_nome}' no mundo {size}x{size}...\n")
    agente.run()

def carregar_benchmark(path):
    """Importa dinamicamente um módulo de benchmark pelo caminho."""
    spec = importlib.util.spec_from_file_location("benchmark_mod", path)
    benchmark_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(benchmark_mod)
    return benchmark_mod.executar_benchmark

def main():
    escolha = menu_interativo()

    if escolha == "1":
        # Benchmark padrão: usa sys.argv[1:] (argumentos do terminal)
        cli_args = sys.argv[1:]
    elif escolha == "5":
        print("\nDigite a linha de comando desejada (exemplo: --agentes logico genetico --sizes 4 6 --execucoes 10 --benchmark outro_benchmark.py):")
        linha = input("main.py ").strip()
        cli_args = shlex.split(linha)
    elif escolha == "2":
        execucao_unica("manual")
        return
    elif escolha == "3":
        execucao_unica("logico")
        return
    elif escolha == "4":
        execucao_unica("genetico")
        return
    else:
        print("Opção inválida.")
        return

    # Só chega aqui se for benchmark (1 ou 5)
    parser = argparse.ArgumentParser(description="Executa benchmarks no Wumpus World")
    parser.add_argument("--execucoes", type=int, default=10, help="Número de execuções por agente/tamanho")
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8], help="Tamanhos do mundo (ex: 4 6 8)")
    parser.add_argument("--agentes", nargs="+", choices=AGENTES_DISPONIVEIS.keys(),
                        default=["logico", "genetico"], help="Agentes a incluir no benchmark")
    parser.add_argument("--benchmark", type=str, default="benchmark.py", help="Arquivo de benchmark a ser usado")
    args = parser.parse_args(cli_args)

    # Carrega o benchmark escolhido pelo usuário
    executar_benchmark = carregar_benchmark(args.benchmark)

    # === Criação do diretório de saída ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("logs", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    resultados = []
    dados_extra = {
        "memoria": [],
        "cpu": [],
        "fitness": [],
        "fitness_pop": [],
        "fitness_final": [],
        "diversidade_vars": [],
        "pop_final": []
    }

    # === Execução dos benchmarks ===
    for size in args.sizes:
        for nome_agente in args.agentes:
            logger = Logger(nome_agente, output_dir)
            logger.write(f"\n🚀 Iniciando benchmark: Agente = '{nome_agente}' | Mundo = {size}x{size}")

            resultado = executar_benchmark(nome_agente, size, args.execucoes)
            resultados.append(resultado)

            if resultado is None:
                print(f"⚠️ Resultado nulo para agente '{nome_agente}' no mundo {size}x{size}")

            # Coleta dados extras (se existirem)
            if nome_agente == "genetico" and isinstance(resultado, dict) and "dados_extra" in resultado:
                # Inicializa dados extras se não existir
                for k in dados_extra:
                    if k in resultado["dados_extra"] and resultado["dados_extra"][k] is not None:
                        dados_extra[k].append(resultado["dados_extra"][k])

            logger.write(f"✅ Benchmark finalizado: '{nome_agente}' no mundo {size}x{size}")
            logger.close()

    # === Salvando e exibindo resultados ===
    df_resultados = pd.DataFrame(resultados)
    csv_path = os.path.join(output_dir, "resultados_benchmark.csv")
    df_resultados.to_csv(csv_path, index=False)
    gerar_graficos(df_resultados, output_dir)

    print(f"\n📊 Resultados salvos em: {csv_path}")
    print(f"📈 Gráficos básicos salvos em: {output_dir}")

    for _, row in df_resultados.iterrows():
        agente = row['agente']
        tamanho = row['tamanho_mundo']
        total = row['vitórias'] + row['mortes'] + row['sobreviveu']
        print(f"\n📊 RESULTADOS - {agente.upper()} | Tamanho: {tamanho}x{tamanho}")
        print(f"🏆 Vitórias: {row['vitórias']} ({(row['vitórias']/total)*100:.1f}%)")
        print(f"☠️ Mortes: {row['mortes']} ({(row['mortes']/total)*100:.1f}%)")
        print(f"🤔 Sobreviveu sem vencer: {row['sobreviveu']} ({(row['sobreviveu']/total)*100:.1f}%)")
        print(f"⏱️ Tempo total: {row['tempo_total']:.2f}s | Tempo médio: {row['tempo_médio']:.3f}s")

    # === Geração de gráficos avançados (se aplicável) ===
    if any(len(v) > 0 for v in dados_extra.values()):
        gerar_graficos_avancados(dados_extra, output_dir)
        print(f"📊 Gráficos avançados salvos em: {output_dir}")

if __name__ == "__main__":
    main()
