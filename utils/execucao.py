# ==============================
# utils/execucao.py
# ==============================
'''
# Executa um agente uma vez e classifica o resultado. Usado pelos 5 benchmarks, para que
# todos tratem erros do mesmo jeito (#30):
#
# - "vitória", "morte" ou "sobreviveu", conforme o estado final do mundo;
# - "erro" se agente.run() lançar uma exceção. Uma execução com erro NÃO conta como vitória,
#   morte ou sobrevivência: ela entra na coluna "erros" do resultado, e o traceback vai para
#   o stderr (que o main.py grava no terminal_output.txt).
'''

import sys
import time
import traceback

STATUS_POSSIVEIS = ("vitória", "morte", "sobreviveu", "erro")


def classificar(mundo):
    """Resultado de uma execução a partir do estado final do mundo."""
    if mundo.won:
        return "vitória"
    if not mundo.is_alive:
        return "morte"
    return "sobreviveu"


def executar_uma(agente, mundo, rotulo=""):
    """
    Roda agente.run() uma vez, sem deixar uma exceção derrubar o benchmark.
    :return: dict com status, tempo (s), resultado devolvido por run() e mensagem de erro (ou None)
    """
    inicio = time.perf_counter()
    try:
        resultado = agente.run()
        erro = None
    except Exception as e:  # o benchmark continua; o erro fica registrado
        resultado = None
        erro = f"{type(e).__name__}: {e}"
        print(f"❌ Erro na execução {rotulo}: {erro}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    tempo = time.perf_counter() - inicio
    return {
        "status": "erro" if erro else classificar(mundo),
        "tempo": tempo,
        "resultado": resultado,
        "erro": erro,
    }


def contar(status):
    """Conta os status no formato do resultado dos benchmarks."""
    return {
        "vitórias": status.count("vitória"),
        "mortes": status.count("morte"),
        "sobreviveu": status.count("sobreviveu"),
        "erros": status.count("erro"),
    }
