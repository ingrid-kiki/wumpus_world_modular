# ==============================
# benchmark.py
# ==============================
"""
# Benchmark do programa: roda um agente em N mundos, com a semente i na execução i, e resume
# vitórias, mortes, sobrevivências, erros e tempos. É usado pelo main.py e substitui os antigos
# benchmark_custom.py, benchmark_fast.py, benchmark_graficos.py e benchmark_sideB.py, que davam
# os mesmos resultados (docs/analise-benchmarks-2026-11.md).
#
# - paralelo=True roda as execuções em processos paralelos (joblib). Compensa em runs longos: o
#   benchmark padrão levou 102 s em paralelo e 258 s em sequência; em runs curtos, iniciar os
#   processos custa alguns segundos a mais.
# - silencioso=True esconde as mensagens de cada execução e de cada passo dos agentes; os erros
#   continuam aparecendo.
#
# Os resultados são os mesmos nos dois modos. tempo_total é o tempo de relógio da combinação, e
# tempo_médio é a média do tempo de cada execução.
"""

import contextlib
import io
import time

from joblib import Parallel, delayed

from agents.registro import AGENTES_AUTOMATICOS, AGENTES_DISPONIVEIS
from utils.execucao import contar, executar_uma, relatar_erro
from world.world import World


def simular_execucao(agente_cls, world_size, seed, parametros=None, silencioso=False, relatar=True, rotulo=""):
    """
    Uma execução: cria o mundo com a semente, roda o agente e classifica o resultado.
    :param relatar: False em outro processo, onde o stderr não chega ao terminal_output.txt;
                    o relato do erro volta em "detalhe_erro" para ser escrito no processo principal (#40)
    """
    mundo = World(size=world_size, seed=seed)
    agente = agente_cls(mundo, **(parametros or {}))
    saida = contextlib.redirect_stdout(io.StringIO()) if silencioso else contextlib.nullcontext()
    with saida:
        # Um erro vira status "erro" e não derruba o benchmark (#30)
        execucao = executar_uma(agente, mundo, rotulo=rotulo or f"com semente {seed}", relatar=relatar)
    resultado = execucao["resultado"]
    return {
        "status": execucao["status"],
        "tempo": execucao["tempo"],
        "dados_extra": resultado.get("dados_extra", {}) if isinstance(resultado, dict) else {},
        "detalhe_erro": execucao["detalhe_erro"],
    }


def resumir(agente_nome, world_size, execucoes, tempo_de_relogio):
    """Resultado de uma combinação de agente e tamanho, no formato que o main.py grava no CSV."""
    return {
        "agente": agente_nome,
        "tamanho_mundo": world_size,
        **contar([e["status"] for e in execucoes]),
        "tempo_total": tempo_de_relogio,
        "tempo_médio": sum(e["tempo"] for e in execucoes) / len(execucoes) if execucoes else 0.0,
        # Dados extras da primeira execução sem erro que os tenha (gráficos avançados e .npz)
        "dados_extra": next((e["dados_extra"] for e in execucoes if e["dados_extra"]), {}),
    }


def executar_benchmark(
    agente_nome, world_size=4, num_execucoes=10, parametros_agentes=None, paralelo=False, silencioso=False
):
    """Roda `num_execucoes` partidas do agente em mundos `world_size` x `world_size` e devolve o resumo."""
    agente_cls = AGENTES_DISPONIVEIS[agente_nome]
    parametros = (parametros_agentes or {}).get(agente_nome, {})
    inicio = time.perf_counter()
    if paralelo:
        execucoes = Parallel(n_jobs=-1)(
            delayed(simular_execucao)(agente_cls, world_size, semente, parametros, silencioso, relatar=False)
            for semente in range(num_execucoes)
        )
        for execucao in execucoes:
            if execucao["detalhe_erro"]:
                relatar_erro(execucao["detalhe_erro"])
    else:
        execucoes = []
        for semente in range(num_execucoes):
            rotulo = f"{semente + 1}/{num_execucoes} [{agente_nome}]"
            if not silencioso:
                print(f"🚀 Execução {rotulo}")
            execucoes.append(simular_execucao(agente_cls, world_size, semente, parametros, silencioso, rotulo=rotulo))
    return resumir(agente_nome, world_size, execucoes, time.perf_counter() - inicio)


if __name__ == "__main__":
    # Só agentes automáticos: o manual pede ações pelo teclado e não faz sentido num benchmark (#30)
    for nome in AGENTES_AUTOMATICOS:
        resultado = executar_benchmark(nome, world_size=4, num_execucoes=3, silencioso=True)
        print(f"\nResumo para {nome}:")
        print(f"Vitórias: {resultado['vitórias']}")
        print(f"Mortes: {resultado['mortes']}")
        print(f"Sobreviveu sem vencer: {resultado['sobreviveu']}")
        print(f"Erros: {resultado['erros']}")
        print(f"Tempo total: {resultado['tempo_total']:.2f}s")
        print(f"Tempo médio por execução: {resultado['tempo_médio']:.3f}s")
