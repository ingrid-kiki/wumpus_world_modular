# ==============================
# tests/test_diagramas.py
# ==============================
"""
# Mantém o diagrama de classes de docs/arquitetura alinhado com o código: toda classe citada
# precisa existir, e toda classe do programa precisa estar no diagrama.
"""

import ast
import os
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIAGRAMA_DE_CLASSES = RAIZ / "docs" / "arquitetura" / "classes.md"

# Pastas que não fazem parte do programa documentado (pastas ocultas, como .venv, são ignoradas sempre)
PASTAS_IGNORADAS = {"__pycache__", "logs", "pygad", "tests", "venv"}

BLOCO_MERMAID = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
DECLARACAO = re.compile(r"^\s*class\s+(\w+)")
# Exemplos: A --> B, A --|> B, A "1" *-- "n" B, A ..> B : usa
RELACAO = re.compile(r'^\s*(\w+)\s+(?:"[^"]*"\s+)?[<|*o.-]+[>|*o.-]*\s+(?:"[^"]*"\s+)?(\w+)')


def classes_do_diagrama(texto):
    """Nomes citados nos blocos classDiagram, em declarações e em relações."""
    citadas = set()
    for bloco in BLOCO_MERMAID.findall(texto.replace("\r\n", "\n")):
        if not bloco.lstrip().startswith("classDiagram"):
            continue
        for linha in bloco.splitlines():
            declaracao, relacao = DECLARACAO.match(linha), RELACAO.match(linha)
            if declaracao:
                citadas.add(declaracao.group(1))
            elif relacao:
                citadas.update(relacao.groups())
    return citadas


def classes_do_codigo(raiz=RAIZ):
    """Classes definidas no nível de módulo nos arquivos .py do programa."""
    classes = set()
    for pasta, subpastas, arquivos in os.walk(raiz):
        subpastas[:] = [nome for nome in subpastas if nome not in PASTAS_IGNORADAS and not nome.startswith(".")]
        for arquivo in arquivos:
            if arquivo.endswith(".py"):
                # Lê em bytes para o Python respeitar a codificação declarada no arquivo
                arvore = ast.parse((Path(pasta) / arquivo).read_bytes())
                classes.update(no.name for no in arvore.body if isinstance(no, ast.ClassDef))
    return classes


def diagrama(corpo):
    return f"# Título\n\n```mermaid\nclassDiagram\n{corpo}\n```\n"


# ---------------------------------------------------------------- Leitura do diagrama


def test_le_classes_declaradas_e_relacoes():
    texto = diagrama('    class World\n    A --|> B\n    C "1" *-- "n" D : tem\n    E ..> F')
    assert classes_do_diagrama(texto) == {"World", "A", "B", "C", "D", "E", "F"}


def test_membros_e_comentarios_nao_contam_como_classes():
    texto = diagrama("    class World {\n        +int size\n        +step(action) str\n    }\n    %% A --> B")
    assert classes_do_diagrama(texto) == {"World"}


def test_ignora_outros_tipos_de_diagrama():
    assert classes_do_diagrama("```mermaid\nflowchart TD\n    A --> B\n```\n") == set()


def test_le_arquivo_com_quebra_de_linha_do_windows():
    assert classes_do_diagrama(diagrama("    class World").replace("\n", "\r\n")) == {"World"}


# ---------------------------------------------------------------- Leitura do código


def test_encontra_classes_do_programa_e_ignora_pastas_de_fora():
    classes = classes_do_codigo()
    assert {"World", "GeneticAlgorithm", "AGVariante", "Agente"} <= classes
    assert "GA" not in classes  # classe principal de pygad/


def test_nao_conta_classe_aninhada(tmp_path):
    (tmp_path / "modulo.py").write_text("class Externa:\n    class Interna:\n        pass\n", encoding="utf-8")
    assert classes_do_codigo(tmp_path) == {"Externa"}


# ---------------------------------------------------------------- Conferência real


def test_diagrama_de_classes_bate_com_o_codigo():
    citadas = classes_do_diagrama(DIAGRAMA_DE_CLASSES.read_text(encoding="utf-8"))
    codigo = classes_do_codigo()
    assert citadas - codigo == set(), "classes citadas no diagrama que não existem no código"
    assert codigo - citadas == set(), "classes do código que faltam no diagrama"
