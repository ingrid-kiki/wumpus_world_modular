# ==============================
# main.py (revisado para menu interativo)
# ==============================

import argparse
import contextlib
import functools
import importlib.util
import io
import os
import shlex
import sys
import traceback
from datetime import datetime

import numpy as np
import pandas as pd

from agents.genetic_agent import GeneticAgent
from agents.registro import AGENTES_AUTOMATICOS, AGENTES_DISPONIVEIS
from utils.graficos import gerar_graficos, gerar_graficos_avancados
from utils.reprodutibilidade import coletar_metadados, parametros_efetivos, salvar_metadados
from utils.terminal import usar_utf8_na_saida
from world.world import TAMANHO_MINIMO, World


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


def perguntar_inteiro(pergunta, minimo=None, opcional=False):
    """Repete a pergunta até receber um inteiro válido; em branco devolve None se for opcional (#38)."""
    while True:
        resposta = input(pergunta).strip()
        if opcional and not resposta:
            return None
        try:
            valor = int(resposta)
        except ValueError:
            print(f"❌ '{resposta}' não é um número inteiro. Tente novamente.")
            continue
        if minimo is not None and valor < minimo:
            print(f"❌ O valor precisa ser {minimo} ou maior. Tente novamente.")
            continue
        return valor


def perguntar_sim_ou_nao(pergunta):
    """True só se a resposta for "s" ou "sim"; em branco ou qualquer outra coisa, False."""
    return input(pergunta).strip().lower() in ("s", "sim")


def mostrar_partida(mundo_inicial, historico):
    """Abre a janela que reproduz a partida; sem pygame ou sem tela, avisa e segue."""
    try:
        from visual.visualizer import Visualizer  # o pygame só é carregado se a janela for pedida

        Visualizer(mundo_inicial).reproduzir(historico)
    except Exception as e:  # a janela é opcional: a partida já terminou e foi mostrada no terminal
        print(f"⚠️ Não foi possível abrir a janela: {type(e).__name__}: {e}")


def execucao_unica(agente_nome):
    """Uma partida de um agente, com tamanho e semente pedidos no menu, e a janela opcional no fim."""
    size = perguntar_inteiro("Tamanho do mundo (ex: 4): ", minimo=TAMANHO_MINIMO)
    seed = perguntar_inteiro("Semente aleatória (opcional, pressione Enter para aleatório): ", opcional=True)

    mundo = World(size=size, seed=seed)
    mundo_inicial = mundo.clone()  # a janela refaz a partida a partir deste estado
    agente = AGENTES_DISPONIVEIS[agente_nome](mundo)

    print(f"\nExecutando agente '{agente_nome}' no mundo {size}x{size}...\n")
    resultado = agente.run()
    if perguntar_sim_ou_nao("\nVer a partida numa janela? (s/N): "):
        mostrar_partida(mundo_inicial, resultado["historico"])


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
            with _gravacao_atomica(os.path.join(output_dir, nome), "wb") as f:
                np.savez_compressed(f, **{chave: np.asarray(valor) for chave, valor in dados_extra.items()})
    df = pd.DataFrame([{k: v for k, v in r.items() if k != "dados_extra"} for r in validos])
    csv_path = os.path.join(output_dir, "resultados_benchmark.csv")
    with _gravacao_atomica(csv_path, "w", encoding="utf-8", newline="") as f:
        df.to_csv(f, index=False)
    return df, csv_path


@contextlib.contextmanager
def _gravacao_atomica(caminho, modo, **kwargs):
    """Grava num arquivo temporário e só então substitui o definitivo: uma queda no meio não corrompe o anterior."""
    temporario = f"{caminho}.tmp"
    with open(temporario, modo, **kwargs) as arquivo:
        yield arquivo
    os.replace(temporario, caminho)


@contextlib.contextmanager
def capturar_saida_terminal(caminho=None):
    """
    Context manager para capturar toda a saída do terminal durante a execução.
    Permite salvar a saída do terminal em um arquivo para análise posterior.
    Captura o stdout e também o stderr, onde ficam os erros e tracebacks das execuções (#30).
    Com `caminho`, grava no arquivo à medida que a execução avança, e um erro que interrompa o
    programa também fica registrado nele: o log sobrevive justamente quando mais é necessário.
    """
    buffer = io.StringIO()
    arquivo = open(caminho, "w", encoding="utf-8") if caminho else None  # noqa: SIM115 (fechado no finally)
    stdout_original, stderr_original = sys.stdout, sys.stderr
    try:

        class DualWriter:
            def __init__(self, terminal, buffer):
                self.terminal = terminal
                self.buffer = buffer

            def write(self, text):
                self.terminal.write(text)
                self.buffer.write(text)
                if arquivo:
                    arquivo.write(text)
                    arquivo.flush()

            def flush(self):
                self.terminal.flush()
                self.buffer.flush()

        sys.stdout = DualWriter(stdout_original, buffer)
        sys.stderr = DualWriter(stderr_original, buffer)
        yield buffer
    except BaseException:  # inclui Ctrl+C; o erro continua subindo normalmente depois de registrado
        if arquivo:
            arquivo.write("\n" + traceback.format_exc())
        raise
    finally:
        sys.stdout, sys.stderr = stdout_original, stderr_original
        if arquivo:
            arquivo.close()


def inteiro_minimo(minimo):
    """Tipo para o argparse: inteiro maior ou igual a `minimo` (#38)."""

    def converter(texto):
        try:
            valor = int(texto)
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{texto}' não é um número inteiro") from None
        if valor < minimo:
            raise argparse.ArgumentTypeError(f"precisa ser {minimo} ou maior (recebido: {valor})")
        return valor

    return converter


def taxa(texto):
    """Tipo para o argparse: número entre 0 e 1 (#38)."""
    try:
        valor = float(texto)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{texto}' não é um número") from None
    if not 0 <= valor <= 1:
        raise argparse.ArgumentTypeError(f"precisa estar entre 0 e 1 (recebido: {valor})")
    return valor


def peso(texto):
    """Tipo para o argparse: número maior ou igual a zero."""
    try:
        valor = float(texto)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{texto}' não é um número") from None
    if valor < 0:
        raise argparse.ArgumentTypeError(f"precisa ser 0 ou maior (recebido: {valor})")
    return valor


def arquivo_existente(caminho):
    """Tipo para o argparse: caminho de um arquivo que existe (#38)."""
    if not os.path.isfile(caminho):
        raise argparse.ArgumentTypeError(f"arquivo não encontrado: {caminho}")
    return caminho


# Parâmetros do GeneticAgent que podem ser passados pela linha de comando (#13)
PARAMETROS_AG_CLI = {
    "populacao": ("population_size", inteiro_minimo(1), "Tamanho da população do AG"),
    "geracoes": ("gens", inteiro_minimo(0), "Número de gerações do AG"),
    "cromossomo": ("chrom_length", inteiro_minimo(1), "Tamanho do cromossomo (ações por indivíduo)"),
    "mutacao": ("mutation_rate", taxa, "Taxa de mutação do AG (0 a 1)"),
    "cruzamento": ("crossover_rate", taxa, "Taxa de cruzamento do AG (0 a 1)"),
    "proximidade": (
        "proximidade",
        peso,
        "Peso do bônus de proximidade ao ouro no fitness (padrão: 0, fitness original; nos experimentos da #31, 20)",
    ),
}


def _opcoes_basicas(parser):
    """Quantas execuções, em que tamanhos, com quais agentes e com qual arquivo de benchmark."""
    parser.add_argument(
        "--execucoes", type=inteiro_minimo(1), default=32, help="Número de execuções por agente/tamanho"
    )
    parser.add_argument(
        "--tamanhos",
        nargs="+",
        type=inteiro_minimo(TAMANHO_MINIMO),
        default=[4, 6, 8],
        help="Tamanhos do mundo (ex: 4 6 8)",
    )
    # O agente manual pede ações pelo teclado: não faz sentido num benchmark (#38)
    parser.add_argument(
        "--agentes",
        nargs="+",
        choices=AGENTES_AUTOMATICOS,
        default=["logico", "genetico"],
        help="Agentes a incluir no benchmark",
    )
    parser.add_argument(
        "--benchmark", type=arquivo_existente, default="benchmark.py", help="Arquivo de benchmark a ser usado"
    )


def _opcoes_dos_agentes(parser):
    """Parâmetros do agente genético e orçamento da busca aleatória."""
    grupo_ag = parser.add_argument_group("agente genético", "Sem estas opções, valem os padrões do GeneticAgent.")
    for opcao, (_, tipo, ajuda) in PARAMETROS_AG_CLI.items():
        grupo_ag.add_argument(f"--{opcao}", type=tipo, default=None, help=ajuda)
    parser.add_argument(
        "--avaliacoes",
        type=inteiro_minimo(1),
        default=None,
        help="Orçamento da busca aleatória (padrão: população x gerações do AG)",
    )


def _opcoes_de_execucao(parser):
    """Como o benchmark roda e onde grava os resultados."""
    parser.add_argument(
        "--paralelo",
        action="store_true",
        help="Roda as execuções em processos paralelos; compensa em runs longos",
    )
    parser.add_argument(
        "--silencioso",
        action="store_true",
        help="Esconde as mensagens de cada execução e de cada passo dos agentes",
    )
    parser.add_argument("--saida", type=str, default=None, help="Pasta de saída (padrão: logs/run_AAAAMMDD_HHMMSS)")


def criar_parser():
    """Linha de comando do benchmark, usada pelas opções 1 e 5 do menu e pelo reproduzir.py."""
    parser = argparse.ArgumentParser(description="Executa benchmarks no Wumpus World")
    _opcoes_basicas(parser)
    _opcoes_dos_agentes(parser)
    _opcoes_de_execucao(parser)
    return parser


def separar_argumentos(linha, windows=os.name == "nt"):
    """
    Separa a linha digitada na opção 5 em argumentos, respeitando aspas.
    No Windows, a barra invertida é separador de caminho: sem isso o shlex a apagaria (#39).
    """
    return shlex.split(linha.replace("\\", "\\\\") if windows else linha)


def parametros_do_ag(args):
    """Parâmetros do GeneticAgent informados na linha de comando (só os que foram passados)."""
    return {
        nome: getattr(args, opcao)
        for opcao, (nome, _, _) in PARAMETROS_AG_CLI.items()
        if getattr(args, opcao) is not None
    }


def main():
    escolha = menu_interativo()

    if escolha == "1":
        # Benchmark padrão: usa sys.argv[1:] (argumentos do terminal)
        cli_args = sys.argv[1:]
    elif escolha == "5":
        print(
            "\nDigite a linha de comando desejada (exemplo: --agentes logico genetico --tamanhos 4 6 --execucoes 10 "
            "--populacao 50 --geracoes 100 --benchmark outro_benchmark.py):"
        )
        linha = input("main.py ").strip()
        cli_args = separar_argumentos(linha)
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


def _parametros_da_busca(args, sobrescritos_ag):
    """A busca aleatória usa o mesmo cromossomo e o mesmo orçamento do AG, para a comparação ser justa (#31)."""
    efetivos_ag = parametros_efetivos(GeneticAgent, sobrescritos_ag)
    return {
        "chrom_length": efetivos_ag["chrom_length"],
        "avaliacoes": args.avaliacoes or efetivos_ag["population_size"] * efetivos_ag["gens"],
    }


def _funcao_de_benchmark(args, sobrescritos_ag, parametros_busca):
    """Função do benchmark escolhido, já com os parâmetros por agente e os modos pedidos."""
    # --paralelo e --silencioso só são repassados quando usados: um benchmark externo sem essas opções continua funcionando
    modos = {opcao: True for opcao in ("paralelo", "silencioso") if getattr(args, opcao)}
    return functools.partial(
        carregar_benchmark(args.benchmark),
        parametros_agentes={"genetico": sobrescritos_ag, "aleatorio": parametros_busca},
        **modos,
    )


def _criar_pasta_do_run(args):
    """Cria a pasta do run: a indicada em --saida ou logs/run_AAAAMMDD_HHMMSS."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.saida or os.path.join("logs", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def _gravar_metadados(cli_args, args, sobrescritos_ag, parametros_busca, output_dir):
    """Grava o metadados.json antes de rodar: se algo falhar, o registro do que foi pedido continua lá."""
    parametros_ag = None
    if "genetico" in args.agentes:
        parametros_ag = parametros_efetivos(GeneticAgent, sobrescritos_ag)
        parametros_ag.pop("seed", None)  # a semente segue a regra descrita em metadados["sementes"]
    metadados = coletar_metadados(cli_args, vars(args), parametros_ag)
    if "aleatorio" in args.agentes:
        metadados["parametros_busca_aleatoria"] = parametros_busca
    salvar_metadados(output_dir, metadados)


def _graficos_avancados_da_combinacao(dados_extra, nome_agente, size, output_dir):
    """Gera os gráficos avançados de uma combinação numa subpasta própria e informa o que saiu."""
    advanced_output_dir = os.path.join(output_dir, f"graficos_avancados_{nome_agente}_{size}x{size}")
    os.makedirs(advanced_output_dir, exist_ok=True)
    relatorio = gerar_graficos_avancados(dados_extra, advanced_output_dir)
    print(
        f"📊 Gráficos avançados para '{nome_agente}' ({size}x{size}): "
        f"{len(relatorio['gerados'])} salvos em {advanced_output_dir}"
    )
    if relatorio["falhas"]:
        print(f"⚠️ Gráficos que falharam: {', '.join(relatorio['falhas'])}")


def _rodar_combinacao(executar_benchmark, nome_agente, size, execucoes, resultados, output_dir):
    """
    Roda um agente num tamanho de mundo e grava o resultado na hora.
    Pastas, arquivos e gravação parcial desta etapa são garantidos por tests/test_main_etapas.py.
    """
    print(f"\n🚀 Iniciando benchmark: Agente = '{nome_agente}' | Mundo = {size}x{size}")
    resultado = executar_benchmark(nome_agente, size, execucoes)
    resultados.append(resultado)
    # Grava a cada etapa: uma queda perde no máximo a etapa em andamento
    salvar_resultados(resultados, output_dir)
    if not isinstance(resultado, dict):  # benchmark externo (--benchmark) sem o contrato
        print(f"⚠️ Resultado nulo para agente '{nome_agente}' no mundo {size}x{size}")
    elif resultado.get("dados_extra"):  # vale para qualquer agente que devolva dados extras
        _graficos_avancados_da_combinacao(resultado["dados_extra"], nome_agente, size, output_dir)
    print(f"✅ Benchmark finalizado: '{nome_agente}' no mundo {size}x{size}")


def _mostrar_resumo(df_resultados):
    """Mostra no terminal as contagens, as porcentagens e os tempos de cada agente e tamanho."""
    for _, row in df_resultados.iterrows():
        agente = row["agente"]
        tamanho = row["tamanho_mundo"]
        erros = row.get("erros", 0)  # benchmarks de terceiros podem não ter a coluna
        total = row["vitorias"] + row["mortes"] + row["sobreviveu"] + erros
        print(f"\n📊 RESULTADOS - {agente.upper()} | Tamanho: {tamanho}x{tamanho}")
        print(f"🏆 Vitórias: {row['vitorias']} ({(row['vitorias'] / total) * 100:.1f}%)")
        print(f"☠️ Mortes: {row['mortes']} ({(row['mortes'] / total) * 100:.1f}%)")
        print(f"🤔 Sobreviveu sem vencer: {row['sobreviveu']} ({(row['sobreviveu'] / total) * 100:.1f}%)")
        if erros:
            print(f"❌ Erros: {erros} ({(erros / total) * 100:.1f}%), detalhes em saida_terminal.txt")
        print(
            f"⏱️ Tempo total: {formatar_tempo(row['tempo_total'])} | Tempo médio: {formatar_tempo(row['tempo_medio'])}"
        )


def rodar_benchmark(cli_args):
    """
    Executa os benchmarks descritos por cli_args e grava tudo na pasta do run, incluindo
    metadados.json (Fase 4 do plano, #17). Usado pelo main() e pelo reproduzir.py.
    :return: (pasta de saída, DataFrame do resumo)
    """
    args = criar_parser().parse_args(cli_args)
    sobrescritos_ag = parametros_do_ag(args)
    parametros_busca = _parametros_da_busca(args, sobrescritos_ag)
    executar_benchmark = _funcao_de_benchmark(args, sobrescritos_ag, parametros_busca)
    output_dir = _criar_pasta_do_run(args)
    _gravar_metadados(cli_args, args, sobrescritos_ag, parametros_busca, output_dir)

    resultados = []
    caminho_saida_terminal = os.path.join(output_dir, "saida_terminal.txt")
    with capturar_saida_terminal(caminho_saida_terminal):
        print(f"🚀 Iniciando benchmark em: {output_dir}")
        print(f"📊 Configuração: {args.execucoes} execuções, tamanhos {args.tamanhos}, agentes {args.agentes}\n")
        for size in args.tamanhos:
            for nome_agente in args.agentes:
                _rodar_combinacao(executar_benchmark, nome_agente, size, args.execucoes, resultados, output_dir)

        df_resultados, csv_path = salvar_resultados(resultados, output_dir)
        gerar_graficos(df_resultados, output_dir)
        print(f"\n📊 Resultados salvos em: {csv_path}")
        print(f"📈 Gráficos básicos salvos em: {output_dir}")
        _mostrar_resumo(df_resultados)

    print(f"\n💾 Saída do terminal salva em: {caminho_saida_terminal}")
    print(f"🧾 Metadados da execução em: {os.path.join(output_dir, 'metadados.json')}")
    return output_dir, df_resultados


if __name__ == "__main__":
    usar_utf8_na_saida()  # a saída redirecionada no Windows não aceitava emojis
    main()
