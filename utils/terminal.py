# ==============================
# utils/terminal.py
# ==============================
"""
# Saída do terminal em UTF-8, para os emojis e acentos das mensagens funcionarem sempre.
#
# No Windows, quando a saída é redirecionada para um arquivo (python main.py > saida.txt) ou
# lida por outro programa, o Python usa a codificação cp1252, que não tem emojis, e a primeira
# mensagem com emoji derrubava o programa com UnicodeEncodeError. Os scripts do projeto chamam
# usar_utf8_na_saida() ao começar; o arquivo redirecionado sai em UTF-8, como o saida_terminal.txt.
"""

import codecs
import sys


def usar_utf8_na_saida():
    """Passa stdout e stderr para UTF-8, se ainda não estiverem; um terminal que já usa UTF-8 não muda."""
    for fluxo in (sys.stdout, sys.stderr):
        codificacao = getattr(fluxo, "encoding", None)
        if not hasattr(fluxo, "reconfigure") or not codificacao:
            continue  # fluxo trocado por outro objeto (por exemplo, nos testes): não é nosso para mudar
        if codecs.lookup(codificacao).name != "utf-8":
            fluxo.reconfigure(encoding="utf-8")
