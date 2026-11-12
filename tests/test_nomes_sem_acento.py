# ==============================
# tests/test_nomes_sem_acento.py
# ==============================
"""
# Regra da Etapa 3 (PR G): nada que o programa grava ou usa como chave pode ter acento.
# Mensagens para as pessoas e a documentação continuam com acentos.
#
# - O ruff (regra PLC2401) barra acentos nos nomes do código: variáveis, funções, classes.
# - test_textos_que_viram_nome_sem_acento barra acentos em textos do código que funcionam como
#   nome: chaves de dicionário, colunas, status, nomes de arquivo e opções de linha de comando.
# - test_saidas_de_um_run_sem_acento roda um benchmark de verdade e confere tudo o que ele grava.
"""

import ast
import contextlib
import io
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

import main
from utils.execucao import STATUS_POSSIVEIS

RAIZ = Path(__file__).resolve().parent.parent
PASTAS_IGNORADAS = {"__pycache__", "logs", "venv", ".venv", ".git"}
# Texto sem espaço e só com letras minúsculas, números, _ . - /: é um nome (chave, coluna, arquivo, opção)
PARECE_NOME = re.compile(r"^[-a-z0-9_./áéíóúâêôãõçà]+$")
# Nomes antigos citados de propósito: o reproduzir.py os traduz ao ler runs gravados até a v1.8.0,
# e os testes montam um run antigo para conferir isso
NOMES_ANTIGOS = {"vitórias", "tempo_médio"}
ARQUIVOS_COM_NOMES_ANTIGOS = {"reproduzir.py", "tests/test_reprodutibilidade.py", "tests/test_nomes_sem_acento.py"}
EXCECOES = {(arquivo, nome) for arquivo in ARQUIVOS_COM_NOMES_ANTIGOS for nome in NOMES_ANTIGOS}


def _tem_acento(texto):
    return not texto.isascii()


def textos_com_acento_que_parecem_nome():
    achados = set()
    for arquivo in sorted(RAIZ.rglob("*.py")):
        relativo = arquivo.relative_to(RAIZ)
        if PASTAS_IGNORADAS & set(relativo.parts):
            continue
        for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
            eh_texto = isinstance(no, ast.Constant) and isinstance(no.value, str)
            if eh_texto and PARECE_NOME.match(no.value) and _tem_acento(no.value):
                achados.add((relativo.as_posix(), no.value))
    return achados


def test_textos_que_viram_nome_sem_acento():
    achados = textos_com_acento_que_parecem_nome() - EXCECOES
    assert not achados, (
        f"Textos usados como nome não podem ter acento (troque, por exemplo, 'vitória' por 'vitoria'): {achados}"
    )


def test_excecoes_ainda_existem():
    """Uma exceção que não aparece mais no código deve sair da lista."""
    assert textos_com_acento_que_parecem_nome() >= EXCECOES


def test_status_sem_acento():
    assert all(status.isascii() for status in STATUS_POSSIVEIS)


def _chaves(valor):
    """Todas as chaves de um JSON, em qualquer nível."""
    if isinstance(valor, dict):
        for chave, item in valor.items():
            yield chave
            yield from _chaves(item)
    elif isinstance(valor, list):
        for item in valor:
            yield from _chaves(item)


def test_saidas_de_um_run_sem_acento(tmp_path):
    pasta = tmp_path / "run"
    argumentos = ["--agentes", "logico", "genetico", "--tamanhos", "4", "--execucoes", "1"]
    argumentos += ["--populacao", "4", "--geracoes", "2", "--cromossomo", "5", "--saida", str(pasta)]
    with contextlib.redirect_stdout(io.StringIO()):
        main.rodar_benchmark(argumentos)

    nomes = [p.relative_to(pasta).as_posix() for p in pasta.rglob("*")]
    assert nomes and all(nome.isascii() for nome in nomes), [n for n in nomes if not n.isascii()]

    colunas = pd.read_csv(pasta / "resultados_benchmark.csv").columns
    assert all(coluna.isascii() for coluna in colunas), list(colunas)

    with np.load(pasta / "dados_extra_genetico_4x4.npz") as dados:
        assert all(chave.isascii() for chave in dados.files), dados.files

    metadados = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    chaves = list(_chaves(metadados))
    assert all(chave.isascii() for chave in chaves), [c for c in chaves if not c.isascii()]
