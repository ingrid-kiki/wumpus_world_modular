# ==============================
# tests/test_lista_de_testes.py
# ==============================
"""
# Mantém docs/testes.md alinhado com os testes: todo teste que o pytest encontra precisa estar na
# lista, com o número certo de casos, e os totais da página precisam bater.
#
# Ao criar, renomear ou remover um teste, atualize docs/testes.md na mesma PR.
"""

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
LISTA = RAIZ / "docs" / "testes.md"
AVISO = "docs/testes.md está desatualizada: atualize a lista na mesma PR que mudou os testes"


@pytest.fixture(scope="module")
def coletados():
    """Identificadores de todos os casos de teste, como o pytest os encontra (ex.: tests/test_x.py::test_y[1])."""
    saida = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )
    return [linha for linha in saida.stdout.splitlines() if "::" in linha]


@pytest.fixture(scope="module")
def lista():
    return LISTA.read_text(encoding="utf-8")


def test_lista_tem_todos_os_testes_com_os_casos_certos(coletados, lista):
    reais = Counter(caso.split("::")[-1].split("[")[0] for caso in coletados)
    documentados = {nome: int(casos) for nome, casos in re.findall(r"^\| `(test_\w+)` \| (\d+) \|", lista, re.M)}
    assert set(reais) - set(documentados) == set(), f"{AVISO}: faltam testes"
    assert set(documentados) - set(reais) == set(), f"{AVISO}: há testes que não existem mais"
    errados = {nome: (documentados[nome], reais[nome]) for nome in reais if documentados[nome] != reais[nome]}
    assert errados == {}, f"{AVISO}: número de casos (lista, real)"


def test_totais_da_lista_batem(coletados, lista):
    por_arquivo = Counter(caso.split("::")[0].split("/")[-1] for caso in coletados)
    resumo = {arquivo: int(casos) for arquivo, casos in re.findall(r"^\| `(test_\w+\.py)` \| (\d+) \|", lista, re.M)}
    assert resumo == dict(por_arquivo), f"{AVISO}: resumo por arquivo"
    funcoes = {caso.split("[")[0] for caso in coletados}
    totais = {
        "casos": int(re.search(r"\*\*(\d+) casos de teste\*\*", lista).group(1)),
        "funções": int(re.search(r"\*\*(\d+) funções\*\*", lista).group(1)),
        "arquivos": int(re.search(r"\*\*(\d+) arquivos\*\*", lista).group(1)),
    }
    assert totais == {"casos": len(coletados), "funções": len(funcoes), "arquivos": len(por_arquivo)}, AVISO
