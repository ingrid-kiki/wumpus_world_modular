# ==============================
# tests/test_saida_redirecionada.py
# ==============================
"""
# Com a saída redirecionada para um arquivo (python main.py > saida.txt), o Windows usa a
# codificação cp1252, que não tem os emojis das mensagens, e o programa quebrava com
# UnicodeEncodeError. PYTHONIOENCODING=cp1252 reproduz essa situação em qualquer sistema.
"""

import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def rodar(argumentos, entrada=""):
    """Roda um script do projeto como um processo novo, com a saída presa a cp1252."""
    ambiente = {**os.environ, "PYTHONIOENCODING": "cp1252", "MPLBACKEND": "Agg"}
    return subprocess.run(
        [sys.executable, *argumentos],
        cwd=RAIZ,
        input=entrada.encode(),
        capture_output=True,
        env=ambiente,
        timeout=60,
    )


def test_benchmark_com_saida_redirecionada_nao_quebra(tmp_path):
    pasta = tmp_path / "run"
    processo = rodar(
        ["main.py", "--agentes", "logico", "--tamanhos", "4", "--execucoes", "1", "--saida", str(pasta)], "1\n"
    )
    assert processo.returncode == 0, processo.stderr.decode("utf-8", "replace")
    assert "🚀 Iniciando benchmark" in processo.stdout.decode("utf-8")

    reproducao = rodar(["reproduzir.py", str(pasta), "--saida", str(tmp_path / "copia")])
    assert reproducao.returncode == 0, reproducao.stderr.decode("utf-8", "replace")
    assert "✅ Resultados idênticos" in reproducao.stdout.decode("utf-8")


def test_partida_do_menu_com_saida_redirecionada_nao_quebra():
    processo = rodar(["main.py"], "3\n4\n1\n\n")  # agente lógico, mundo 4x4, semente 1, sem janela
    assert processo.returncode == 0, processo.stderr.decode("utf-8", "replace")
    assert "Executando agente 'logico'" in processo.stdout.decode("utf-8")
