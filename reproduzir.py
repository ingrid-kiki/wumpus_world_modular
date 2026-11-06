# ==============================
# reproduzir.py
# ==============================
'''
# Refaz uma execução de benchmark a partir do metadata.json gravado na pasta do run
# e compara os resultados com os originais.
#
# Uso:
#     python reproduzir.py logs/run_AAAAMMDD_HHMMSS
#     python reproduzir.py logs/run_AAAAMMDD_HHMMSS --saida logs/reproducao
#
# Vitórias, mortes e sobrevivências devem ser idênticas (as sementes são fixas).
# Tempos, memória e CPU variam de máquina para máquina e não são comparados.
# Código de saída: 0 se os resultados batem, 1 se diferem, 2 se não foi possível comparar.
'''

import argparse
import os
import sys

import pandas as pd

from utils.reprodutibilidade import carregar_metadados, estado_do_git, versoes_das_bibliotecas
from utils.versao import __version__

COLUNAS_COMPARADAS = ["agente", "tamanho_mundo", "vitórias", "mortes", "sobreviveu"]


def sem_opcao(argumentos, opcao):
    """Remove uma opção e seu valor de uma lista de argumentos de linha de comando."""
    saida, pular = [], False
    for arg in argumentos:
        if pular:
            pular = False
            continue
        if arg == opcao:
            pular = True
            continue
        if arg.startswith(opcao + "="):
            continue
        saida.append(arg)
    return saida


def avisos_de_ambiente(meta):
    """Diferenças de código ou de ambiente que podem explicar resultados diferentes."""
    avisos = []
    git_atual, git_original = estado_do_git(), meta.get("git") or {}
    if git_original.get("commit") and git_atual["commit"] != git_original["commit"]:
        avisos.append(f"commit diferente: original {git_original['commit'][:7]}, atual {str(git_atual['commit'])[:7]}")
    if git_original.get("alteracoes_nao_commitadas"):
        avisos.append("a execução original tinha alterações não commitadas: "
                      + ", ".join(git_original.get("arquivos_alterados", [])))
    if git_atual.get("alteracoes_nao_commitadas"):
        avisos.append("há alterações não commitadas agora: " + ", ".join(git_atual["arquivos_alterados"]))
    if meta.get("versao") != __version__:
        avisos.append(f"versão diferente: original {meta.get('versao')}, atual {__version__}")
    atuais = versoes_das_bibliotecas()
    for nome, versao in (meta.get("bibliotecas") or {}).items():
        if atuais.get(nome) != versao:
            avisos.append(f"{nome}: original {versao}, atual {atuais.get(nome)}")
    return avisos


def comparar(csv_original, csv_novo):
    """Devolve (iguais, tabela) comparando só as colunas determinísticas."""
    a, b = pd.read_csv(csv_original), pd.read_csv(csv_novo)
    # "erros" existe a partir da v1.6.0 (#30); só entra na comparação se os dois CSVs tiverem
    colunas = COLUNAS_COMPARADAS + (["erros"] if "erros" in a.columns and "erros" in b.columns else [])
    a, b = a[colunas], b[colunas]
    tabela = a.merge(b, on=["agente", "tamanho_mundo"], how="outer", suffixes=("_original", "_reproducao"))
    iguais = len(a) == len(b) and a.sort_values(["agente", "tamanho_mundo"]).reset_index(drop=True).equals(
        b.sort_values(["agente", "tamanho_mundo"]).reset_index(drop=True))
    return iguais, tabela


def main(argv=None):
    parser = argparse.ArgumentParser(description="Refaz um benchmark a partir do metadata.json e compara os resultados")
    parser.add_argument("pasta", help="Pasta do run original (contém metadata.json e resultados_benchmark.csv)")
    parser.add_argument("--saida", default=None, help="Pasta para a reprodução (padrão: <pasta>_reproducao)")
    args = parser.parse_args(argv)

    try:
        meta = carregar_metadados(args.pasta)
    except FileNotFoundError:
        print(f"❌ {args.pasta} não tem metadata.json (runs anteriores à v1.5.0 não têm).")
        return 2
    csv_original = os.path.join(args.pasta, "resultados_benchmark.csv")
    if not os.path.exists(csv_original):
        print(f"❌ {csv_original} não existe: a execução original não terminou.")
        return 2

    avisos = avisos_de_ambiente(meta)
    for aviso in avisos:
        print(f"⚠️ {aviso}")

    saida = args.saida or args.pasta.rstrip("/\\") + "_reproducao"
    argumentos = sem_opcao(meta["argumentos_cli"], "--saida") + ["--saida", saida]
    print(f"🔁 Reproduzindo: main.py {' '.join(argumentos)}\n")

    import main as programa  # importado aqui para os avisos aparecerem antes das mensagens do benchmark
    programa.rodar_benchmark(argumentos)

    iguais, tabela = comparar(csv_original, os.path.join(saida, "resultados_benchmark.csv"))
    print("\n" + tabela.to_string(index=False))
    if iguais:
        print("\n✅ Resultados idênticos aos originais.")
        return 0
    print("\n❌ Resultados diferentes dos originais." + (" Veja os avisos acima." if avisos else ""))
    return 1


if __name__ == "__main__":
    sys.exit(main())
