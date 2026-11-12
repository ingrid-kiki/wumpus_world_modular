# ==============================
# tests/test_constantes.py
# ==============================
"""
# As ações, percepções e status do jogo ficam só em world/constantes.py. Estes testes impedem
# que a ordem das ações mude sem querer (ela define os sorteios dos experimentos) e que as listas
# voltem a ser escritas à mão em outros arquivos.
"""

import ast
import os
from pathlib import Path

from world import constantes

RAIZ = Path(__file__).resolve().parent.parent
PASTAS_IGNORADAS = {"__pycache__", "logs", "pygad", "tests", "venv"}
VALORES = {
    *constantes.ACOES,
    constantes.FEDOR,
    constantes.BRISA,
    constantes.BRILHO,
    constantes.OK,
    constantes.MORTO,
    constantes.GANHOU,
}


def test_ordem_das_acoes_nao_muda():
    assert constantes.ACOES == ("CIMA", "BAIXO", "ESQUERDA", "DIREITA", "AGARRAR", "TIRO")


def test_deslocamentos_cobrem_os_movimentos_na_mesma_ordem():
    assert tuple(constantes.DESLOCAMENTOS) == constantes.ACOES_DE_MOVIMENTO
    assert sorted(constantes.DESLOCAMENTOS.values()) == [(-1, 0), (0, -1), (0, 1), (1, 0)]


def test_nenhum_arquivo_escreve_acoes_percepcoes_ou_status_a_mao():
    """Fora de world/constantes.py, esses valores só podem aparecer pelas constantes."""
    encontrados = []
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [nome for nome in subpastas if nome not in PASTAS_IGNORADAS and not nome.startswith(".")]
        for arquivo in arquivos:
            caminho = Path(pasta) / arquivo
            if not arquivo.endswith(".py") or caminho == RAIZ / "world" / "constantes.py":
                continue
            for no in ast.walk(ast.parse(caminho.read_bytes())):
                if isinstance(no, ast.Constant) and no.value in VALORES:
                    encontrados.append(f"{caminho.relative_to(RAIZ).as_posix()}:{no.lineno} {no.value}")
    assert encontrados == []
