# ==============================
# main.py (revisado para menu interativo)
# ==============================
'''
# Este arquivo é o ponto de entrada do projeto Wumpus World.
# Ele oferece um menu interativo para o usuário escolher entre diferentes modos de execução:
# - Benchmark com vários agentes e tamanhos de mundo
# - Execução manual, lógica ou genética individual
# - Execução customizada via linha de comando (CLI)
# O script gerencia a configuração dos experimentos, coleta resultados, gera logs e gráficos.
'''

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
from utils.advance_graphs import gerar_graficos, gerar_graficos_avancados
from benchmark.bm import executar_benchmark

# Dicionário de agentes disponíveis para seleção no menu e benchmarks
AGENTES_DISPONIVEIS = {
    "manual": ManualAgent,
    "logico": LogicAgent,
    "genetico": GeneticAgent
}

def menu_interativo():
    """
    Exibe o menu principal e retorna a escolha do usuário.
    """
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
    """
    Executa um agente único (manual, lógico ou genético) em modo interativo.
    Solicita ao usuário o tamanho do mundo e a semente (opcional).
    """
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
    """
    Importa dinamicamente um módulo de benchmark pelo caminho informado.
    Permite usar diferentes arquivos de benchmark.
    """
    # Se não for caminho absoluto e não começar com 'benchmark/', corrija
    if not os.path.isabs(path) and not path.startswith("benchmark/"):
        path = os.path.join("benchmark", path)
    if not os.path.isabs(path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, path)
    spec = importlib.util.spec_from_file_location("benchmark_mod", path)
    benchmark_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(benchmark_mod)
    return benchmark_mod.executar_benchmark

class Tee:
    """
    Redireciona tudo que é impresso no terminal para também ser salvo em um arquivo.
    """
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

def main():
    """
    Função principal do programa.
    Gerencia o menu, coleta argumentos, executa benchmarks, salva resultados e gera gráficos.
    """
    escolha = menu_interativo()

    # Define os argumentos de linha de comando conforme a escolha do usuário
    if escolha == "1":
        # Benchmark padrão: usa sys.argv[1:] (argumentos do terminal)
        cli_args = sys.argv[1:]
    elif escolha == "5":
        print("\nDigite a linha de comando desejada (exemplo: --agentes logico genetico --sizes 4 6 --execucoes 10 --benchmark bm_algum.py):")
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
    parser.add_argument("--benchmark", type=str, default="benchmark/bm_padrao.py", help="Arquivo de benchmark a ser usado")
    args = parser.parse_args(cli_args)

    # Carrega o benchmark escolhido pelo usuário (pode ser customizado)
    executar_benchmark = carregar_benchmark(args.benchmark)

    # === Criação do diretório de saída para logs e resultados ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(BASE_DIR, "logs", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    # Caminho do arquivo de log geral
    log_path = os.path.join(output_dir, "saida_terminal.log")
    log_file = open(log_path, "w", encoding="utf-8")
    sys.stdout = Tee(sys.stdout, log_file)
    sys.stderr = Tee(sys.stderr, log_file)  # Opcional: salva também erros

    resultados = []
    # Estrutura para armazenar dados extras dos agentes (ex: fitness do genético)
    dados_extra = {
        "memoria": [],
        "cpu": [],
        "fitness": [],
        "fitness_pop": [],
        "fitness_final": [],
        "diversidade_vars": [],
        "pop_final": []
    }

    # === Execução dos benchmarks para cada agente e tamanho de mundo ===
    for size in args.sizes:
        for nome_agente in args.agentes:
            logger = Logger(nome_agente, output_dir)
            logger.write(f"\n🚀 Iniciando benchmark: Agente = '{nome_agente}' | Mundo = {size}x{size}")

            resultado = executar_benchmark(nome_agente, size, args.execucoes)
            resultados.append(resultado)

            if resultado is None:
                print(f"⚠️ Resultado nulo para agente '{nome_agente}' no mundo {size}x{size}")

            # Coleta dados extras (se existirem) para o agente genético
            if nome_agente == "genetico" and isinstance(resultado, dict) and "dados_extra" in resultado:
                # Inicializa dados extras se não existir
                for k in dados_extra:
                    if k in resultado["dados_extra"] and resultado["dados_extra"][k] is not None:
                        dados_extra[k].append(resultado["dados_extra"][k])

            logger.write(f"✅ Benchmark finalizado: '{nome_agente}' no mundo {size}x{size}")
            logger.close()

    # === Salvando e exibindo resultados em CSV e gráficos ===
    df_resultados = pd.DataFrame(resultados)
    csv_path = os.path.join(output_dir, "resultados_benchmark.csv")
    df_resultados.to_csv(csv_path, index=False)
    gerar_graficos(df_resultados, output_dir)

    print(f"\n📊 Resultados salvos em: {csv_path}")
    print(f"📈 Gráficos básicos salvos em: {output_dir}")

    # Exibe resumo dos resultados no terminal
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

    if log_file:
        log_file.close()

if __name__ == "__main__":
    main()
