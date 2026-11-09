# ==============================
# utils/reprodutibilidade.py
# ==============================
"""
# Registra, junto com cada execução de benchmark, tudo o que é preciso para refazê-la:
# versão e commit do código, argumentos usados, parâmetros efetivos do agente genético,
# regra das sementes e versões do Python e das bibliotecas.
#
# O arquivo metadata.json fica na pasta do run (logs/run_AAAAMMDD_HHMMSS/) e é lido
# por reproduzir.py.
"""

import inspect
import json
import os
import platform
import subprocess
import sys
from datetime import datetime
from importlib import metadata

from utils.versao import __version__

# Bibliotecas cujas versões influenciam os resultados ou os gráficos
BIBLIOTECAS = ["numpy", "pandas", "matplotlib", "seaborn", "scikit-learn", "joblib", "psutil", "pygame", "pygad"]

# Descrição de como as sementes são usadas (vale para todos os benchmarks do projeto)
REGRA_DAS_SEMENTES = (
    "Execução i (i = 0 .. execucoes-1) usa World(size, seed=i). "
    "O agente genético, sem semente explícita, usa a semente do mundo."
)


def _git(*args, cwd=None):
    """Roda um comando git e devolve a saída, ou None se o git não estiver disponível."""
    try:
        saida = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True, timeout=10)
        # Só tira a quebra de linha final: no 'status --porcelain' o espaço inicial faz parte do formato
        return saida.stdout.rstrip("\n")
    except (OSError, subprocess.SubprocessError):
        return None


def estado_do_git(cwd=None):
    """
    Commit atual e se há alterações não commitadas em arquivos versionados.
    Arquivos ignorados (logs/, .venv/) e não versionados não contam.
    """
    commit = _git("rev-parse", "HEAD", cwd=cwd)
    if commit is None:
        return {"commit": None, "branch": None, "alteracoes_nao_commitadas": None, "arquivos_alterados": []}
    alterados = _git("status", "--porcelain", "--untracked-files=no", cwd=cwd) or ""
    arquivos = [linha[3:] for linha in alterados.splitlines() if linha.strip()]
    return {
        "commit": commit,
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd),
        "alteracoes_nao_commitadas": bool(arquivos),
        "arquivos_alterados": arquivos,
    }


def versoes_das_bibliotecas(nomes=BIBLIOTECAS):
    versoes = {}
    for nome in nomes:
        try:
            versoes[nome] = metadata.version(nome)
        except metadata.PackageNotFoundError:
            versoes[nome] = None
    return versoes


def parametros_efetivos(classe, sobrescritos=None):
    """Valores padrão do __init__ da classe, com os sobrescritos aplicados por cima."""
    assinatura = inspect.signature(classe.__init__)
    padroes = {nome: p.default for nome, p in assinatura.parameters.items() if p.default is not inspect.Parameter.empty}
    padroes.update(sobrescritos or {})
    return padroes


def coletar_metadados(argumentos_cli, argumentos, parametros_ag, cwd=None):
    """
    Monta o dicionário salvo em metadata.json.
    :param argumentos_cli: lista de argumentos como digitados (ex.: ["--sizes", "4", "6"])
    :param argumentos: dict com os argumentos já interpretados (vars(args))
    :param parametros_ag: parâmetros efetivos do GeneticAgent (ou None se ele não rodou)
    """
    return {
        "versao": __version__,
        "data_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
        "git": estado_do_git(cwd),
        "argumentos_cli": list(argumentos_cli),
        "argumentos": argumentos,
        "parametros_ag": parametros_ag,
        "sementes": REGRA_DAS_SEMENTES,
        "python": sys.version.split()[0],
        "plataforma": platform.platform(),
        "bibliotecas": versoes_das_bibliotecas(),
    }


def salvar_metadados(pasta, metadados):
    caminho = os.path.join(pasta, "metadata.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(metadados, f, ensure_ascii=False, indent=2, default=str)
    return caminho


def carregar_metadados(pasta):
    with open(os.path.join(pasta, "metadata.json"), encoding="utf-8") as f:
        return json.load(f)
