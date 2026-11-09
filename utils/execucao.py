# ==============================
# utils/execucao.py
# ==============================
"""
# Executa um agente uma vez e classifica o resultado. Usado pelos 5 benchmarks, para que
# todos tratem erros do mesmo jeito (#30):
#
# - "vitória", "morte" ou "sobreviveu", conforme o estado final do mundo;
# - "erro" se agente.run() lançar uma exceção. Uma execução com erro NÃO conta como vitória,
#   morte ou sobrevivência: ela entra na coluna "erros" do resultado, e o traceback vai para
#   o stderr (que o main.py grava no terminal_output.txt).
"""

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


def relatar_erro(detalhe):
    """Escreve o relato de um erro no stderr, que o main.py grava no terminal_output.txt."""
    print(detalhe, file=sys.stderr)


def executar_uma(agente, mundo, rotulo="", relatar=True):
    """
    Roda agente.run() uma vez, sem deixar uma exceção derrubar o benchmark.
    :param relatar: False quando a execução roda em outro processo: o stderr de lá não chega ao
                    terminal_output.txt, então quem chamou deve usar relatar_erro(execucao["detalhe_erro"]) (#40)
    :return: dict com status, tempo (s), resultado devolvido por run(), mensagem de erro e relato completo (ou None)
    """
    inicio = time.perf_counter()
    detalhe = None
    try:
        resultado = agente.run()
        erro = None
    except Exception as e:  # o benchmark continua; o erro fica registrado
        resultado = None
        erro = f"{type(e).__name__}: {e}"
        detalhe = f"❌ Erro na execução {rotulo}: {erro}\n{traceback.format_exc()}"
        if relatar:
            relatar_erro(detalhe)
    tempo = time.perf_counter() - inicio
    return {
        "status": "erro" if erro else classificar(mundo),
        "tempo": tempo,
        "resultado": resultado,
        "erro": erro,
        "detalhe_erro": detalhe,
    }


def contar(status):
    """Conta os status no formato do resultado dos benchmarks."""
    return {
        "vitórias": status.count("vitória"),
        "mortes": status.count("morte"),
        "sobreviveu": status.count("sobreviveu"),
        "erros": status.count("erro"),
    }
