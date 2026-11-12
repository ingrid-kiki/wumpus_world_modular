# ==============================
# tests/test_tamanho_das_funcoes.py
# ==============================
"""
# Metas de código limpo da Etapa 3: nenhuma função do programa passa de 40 linhas, e a única
# exceção de complexidade permitida é a que ainda espera a sua PR.
"""

import ast
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTAS_IGNORADAS = {"__pycache__", "logs", "pygad", "tests", "venv"}
LIMITE_DE_LINHAS = 40
# draw_world será dividida junto com a ligação do Visualizer ao --vis (PR F da Etapa 3)
EXCECOES = {"visual/visualizer.py:draw_world"}


def arquivos_do_programa():
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [nome for nome in subpastas if nome not in PASTAS_IGNORADAS and not nome.startswith(".")]
        for arquivo in arquivos:
            if arquivo.endswith(".py"):
                caminho = Path(pasta) / arquivo
                yield caminho.relative_to(RAIZ).as_posix(), caminho


def test_nenhuma_funcao_passa_de_40_linhas():
    longas = []
    for nome, caminho in arquivos_do_programa():
        for no in ast.walk(ast.parse(caminho.read_bytes())):
            if isinstance(no, ast.FunctionDef | ast.AsyncFunctionDef):
                linhas = no.end_lineno - no.lineno + 1
                if linhas > LIMITE_DE_LINHAS and f"{nome}:{no.name}" not in EXCECOES:
                    longas.append(f"{nome}:{no.name} ({linhas} linhas)")
    assert longas == []


def test_excecoes_de_complexidade_so_onde_registrado():
    com_excecao = {
        nome for nome, caminho in arquivos_do_programa() if "noqa: C901" in caminho.read_text(encoding="utf-8")
    }
    assert com_excecao <= {excecao.split(":")[0] for excecao in EXCECOES}
