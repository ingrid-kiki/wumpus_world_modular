# ==============================
# tests/regras/test_tipos.py
# ==============================
"""
# Regra da Etapa 3 (PR H): toda função pública do programa tem tipos nos parâmetros e no retorno.
# O mypy (no CI e no pre-commit) confere se os tipos estão certos; este teste garante que eles
# existem, porque o mypy aceita uma função sem nenhum tipo.
#
# Pública é a função cujo nome não começa com "_"; o __init__ também entra, porque é o
# construtor que as outras partes do programa chamam.
"""

import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
PASTAS_IGNORADAS = {"__pycache__", "logs", "venv", ".venv", ".git", "tests"}


def funcoes_publicas_sem_tipos(raiz=RAIZ):
    faltando = []
    for arquivo in sorted(raiz.rglob("*.py")):
        relativo = arquivo.relative_to(raiz)
        if PASTAS_IGNORADAS & set(relativo.parts):
            continue
        for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
            if not isinstance(no, ast.FunctionDef) or (no.name.startswith("_") and no.name != "__init__"):
                continue
            argumentos = no.args.posonlyargs + no.args.args + no.args.kwonlyargs
            sem_tipo = [a.arg for a in argumentos if a.annotation is None and a.arg not in ("self", "cls")]
            sem_tipo += [f"*{a.arg}" for a in (no.args.vararg, no.args.kwarg) if a is not None and a.annotation is None]
            if no.returns is None:
                sem_tipo.append("retorno")
            if sem_tipo:
                faltando.append(f"{relativo.as_posix()}:{no.lineno} {no.name} ({', '.join(sem_tipo)})")
    return faltando


def test_funcoes_publicas_tem_tipos():
    faltando = funcoes_publicas_sem_tipos()
    assert faltando == [], "Funções públicas sem tipos (nos parâmetros ou no retorno):\n" + "\n".join(faltando)


def test_regra_acusa_funcao_sem_tipos(tmp_path):
    (tmp_path / "modulo.py").write_text(
        "def publica(a, b: int):\n    return a\n\n"
        "def _privada(a):\n    return a\n\n"
        "class C:\n    def __init__(self, x):\n        self.x = x\n\n"
        "    def certo(self, y: int) -> int:\n        return y\n",
        encoding="utf-8",
    )
    assert funcoes_publicas_sem_tipos(tmp_path) == [
        "modulo.py:1 publica (a, retorno)",
        "modulo.py:8 __init__ (x, retorno)",
    ]
