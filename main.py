# ==============================
# main.py (revisado para menu interativo)
# ==============================

import argparse
import functools
import os
import sys
from datetime import datetime
import numpy as np
import pandas as pd
import shlex
import importlib.util
import io
import contextlib

from world.world import World
from agents.manual_agent import ManualAgent
from agents.logic_agent import LogicAgent
from agents.genetic_agent import GeneticAgent
from utils.logger import Logger
from utils.graficos import gerar_graficos, gerar_graficos_avancados
from utils.reprodutibilidade import coletar_metadados, parametros_efetivos, salvar_metadados

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

def formatar_tempo(segundos):
    """
    Formata tempo em segundos para uma string legível.
    Retorna em minutos se >= 60s, senão em segundos.
    """
    if segundos >= 60:
        minutos = segundos / 60
        return f"{minutos:.2f} min"
    else:
        return f"{segundos:.2f}s"

def salvar_resultados(resultados, output_dir):
    """
    Salva o resumo dos benchmarks em resultados_benchmark.csv, só com colunas escalares.
    Os dados extras (arrays do AG) vão para dados_extra_<agente>_<N>x<N>.npz, um arquivo por
    agente e tamanho: no CSV eles viravam uma string truncada com "..." (#24).
    :return: (DataFrame do resumo, caminho do CSV)
    """
    validos = [r for r in resultados if isinstance(r, dict)]
    for r in validos:
        dados_extra = r.get("dados_extra")
        if dados_extra:
            nome = f"dados_extra_{r['agente']}_{r['tamanho_mundo']}x{r['tamanho_mundo']}.npz"
            np.savez_compressed(os.path.join(output_dir, nome),
                                **{chave: np.asarray(valor) for chave, valor in dados_extra.items()})
    df = pd.DataFrame([{k: v for k, v in r.items() if k != "dados_extra"} for r in validos])
    csv_path = os.path.join(output_dir, "resultados_benchmark.csv")
    df.to_csv(csv_path, index=False)
    return df, csv_path

@contextlib.contextmanager
def capturar_saida_terminal():
    """
    Context manager para capturar toda a saída do terminal durante a execução.
    Permite salvar a saída do terminal em um arquivo para análise posterior.
    """
    buffer = io.StringIO()
    stdout_original = sys.stdout
    try:
        class DualWriter:
            def __init__(self, terminal, buffer):
                self.terminal = terminal
                self.buffer = buffer
            def write(self, text):
                self.terminal.write(text)
                self.buffer.write(text)
            def flush(self):
                self.terminal.flush()
                self.buffer.flush()
        sys.stdout = DualWriter(stdout_original, buffer)
        yield buffer
    finally:
        sys.stdout = stdout_original

# Parâmetros do GeneticAgent que podem ser passados pela linha de comando (#13)
PARAMETROS_AG_CLI = {
    "populacao": ("population_size", int, "Tamanho da população do AG"),
    "geracoes": ("gens", int, "Número de gerações do AG"),
    "cromossomo": ("chrom_length", int, "Tamanho do cromossomo (ações por indivíduo)"),
    "mutacao": ("mutation_rate", float, "Taxa de mutação do AG (0 a 1)"),
    "cruzamento": ("crossover_rate", float, "Taxa de cruzamento do AG (0 a 1)"),
}

def criar_parser():
    parser = argparse.ArgumentParser(description="Executa benchmarks no Wumpus World")
    parser.add_argument("--execucoes", type=int, default=32, help="Número de execuções por agente/tamanho")
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8], help="Tamanhos do mundo (ex: 4 6 8)")
    parser.add_argument("--agentes", nargs="+", choices=AGENTES_DISPONIVEIS.keys(),
                        default=["logico", "genetico"], help="Agentes a incluir no benchmark")
    parser.add_argument("--benchmark", type=str, default="benchmark.py", help="Arquivo de benchmark a ser usado")
    grupo_ag = parser.add_argument_group("agente genético", "Sem estas opções, valem os padrões do GeneticAgent.")
    for opcao, (_, tipo, ajuda) in PARAMETROS_AG_CLI.items():
        grupo_ag.add_argument(f"--{opcao}", type=tipo, default=None, help=ajuda)
    parser.add_argument("--saida", type=str, default=None,
                        help="Pasta de saída (padrão: logs/run_AAAAMMDD_HHMMSS)")
    return parser

def parametros_do_ag(args):
    """Parâmetros do GeneticAgent informados na linha de comando (só os que foram passados)."""
    return {nome: getattr(args, opcao) for opcao, (nome, _, _) in PARAMETROS_AG_CLI.items()
            if getattr(args, opcao) is not None}

def main():
    escolha = menu_interativo()

    if escolha == "1":
        # Benchmark padrão: usa sys.argv[1:] (argumentos do terminal)
        cli_args = sys.argv[1:]
    elif escolha == "5":
        print("\nDigite a linha de comando desejada (exemplo: --agentes logico genetico --sizes 4 6 --execucoes 10 "
              "--populacao 50 --geracoes 100 --benchmark outro_benchmark.py):")
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
    rodar_benchmark(cli_args)

def rodar_benchmark(cli_args):
    """
    Executa os benchmarks descritos por cli_args e grava tudo na pasta do run, incluindo
    metadata.json (Fase 4 do plano, #17). Usado pelo main() e pelo reproduzir.py.
    :return: (pasta de saída, DataFrame do resumo)
    """
    args = criar_parser().parse_args(cli_args)
    sobrescritos_ag = parametros_do_ag(args)

    # Carrega o benchmark escolhido pelo usuário; os parâmetros por agente vão junto em toda chamada
    executar_benchmark = functools.partial(carregar_benchmark(args.benchmark),
                                           parametros_agentes={"genetico": sobrescritos_ag})

    # === Criação do diretório de saída ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.saida or os.path.join("logs", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    # === Metadados da execução, gravados antes de rodar (se algo falhar, fica o registro) ===
    parametros_ag = None
    if "genetico" in args.agentes:
        parametros_ag = parametros_efetivos(GeneticAgent, sobrescritos_ag)
        parametros_ag.pop("seed", None)  # a semente segue a regra descrita em metadados["sementes"]
    salvar_metadados(output_dir, coletar_metadados(cli_args, vars(args), parametros_ag))

    resultados = []

    # === Execução dos benchmarks ===
    with capturar_saida_terminal() as buffer:
        print(f"🚀 Iniciando benchmark em: {output_dir}")
        print(f"📊 Configuração: {args.execucoes} execuções, tamanhos {args.sizes}, agentes {args.agentes}\n")

        for size in args.sizes:
            for nome_agente in args.agentes:
                logger = Logger(nome_agente, output_dir)
                logger.write(f"\n🚀 Iniciando benchmark: Agente = '{nome_agente}' | Mundo = {size}x{size}")

                # ATENÇÃO: NÃO ALTERAR A SEÇÃO DE DADOS EXTRAS E GRÁFICOS AVANÇADOS
                resultado = executar_benchmark(nome_agente, size, args.execucoes)
                resultados.append(resultado)

                if resultado is None:
                    print(f"⚠️ Resultado nulo para agente '{nome_agente}' no mundo {size}x{size}")

                # Salva dados extras e gráficos avançados
                if nome_agente == "genetico" and isinstance(resultado, dict) and "dados_extra" in resultado and resultado["dados_extra"]:
                    advanced_output_dir = os.path.join(output_dir, f"advanced_charts_{nome_agente}_{size}x{size}")
                    os.makedirs(advanced_output_dir, exist_ok=True)
                    gerar_graficos_avancados(resultado["dados_extra"], advanced_output_dir)
                    print(f"📊 Gráficos avançados para '{nome_agente}' ({size}x{size}) salvos em: {advanced_output_dir}")

                logger.write(f"✅ Benchmark finalizado: '{nome_agente}' no mundo {size}x{size}")
                logger.close()

        df_resultados, csv_path = salvar_resultados(resultados, output_dir)
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
            print(f"⏱️ Tempo total: {formatar_tempo(row['tempo_total'])} | Tempo médio: {formatar_tempo(row['tempo_médio'])}")

    # === Salvando a saída do terminal em arquivo .txt ===
    terminal_output_path = os.path.join(output_dir, "terminal_output.txt")
    with open(terminal_output_path, "w", encoding="utf-8") as f:
        f.write(buffer.getvalue())

    print(f"\n💾 Saída do terminal salva em: {terminal_output_path}")
    print(f"🧾 Metadados da execução em: {os.path.join(output_dir, 'metadata.json')}")
    return output_dir, df_resultados

if __name__ == "__main__":
    main()