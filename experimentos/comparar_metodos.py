# ==============================
# experimentos/comparar_metodos.py
# ==============================
"""
# Investigação da issue #31: o agente genético supera a busca aleatória?
#
# Compara métodos de busca nos mesmos mundos e com o mesmo orçamento de avaliações de fitness.
# A comparação é pareada por mundo: para cada par de métodos, usa o teste exato de McNemar sobre
# os mundos em que só um dos dois venceu, com correção de Holm para comparações múltiplas.
#
# Uso (a partir da raiz do projeto):
#     python -m experimentos.comparar_metodos --fase confirmacao
#     python -m experimentos.comparar_metodos --fase hipoteses
#     python -m experimentos.comparar_metodos --fase padrao     (100 x 500 x 100, 50.000 avaliações)
#     python -m experimentos.comparar_metodos --fase confirmacao --mundos 20    (teste rápido)
#
# Saída em logs/exp31_<fase>_AAAAMMDD_HHMMSS/: tentativas.csv (uma linha por método e mundo),
# resumo.csv, comparacoes.csv e metadata.json.
"""

import argparse
import itertools
import json
import os
import random
import time
from collections import deque
from datetime import datetime

import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import binomtest

from ga.ga_core import GeneticAlgorithm
from ga.individual import Individual
from utils.reprodutibilidade import estado_do_git, versoes_das_bibliotecas
from utils.versao import __version__
from world.world import World

ACOES = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA", "AGARRAR", "TIRO"]
REFERENCIA = "busca_aleatoria"


def resolvivel(mundo):
    """True se existe caminho até o ouro sem pisar em poço (o Wumpus pode ser morto com um tiro)."""
    fila, vistos = deque([(0, 0)]), {(0, 0)}
    while fila:
        x, y = fila.popleft()
        if (x, y) == mundo.gold_pos:
            return True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            viz = (x + dx, y + dy)
            if 0 <= viz[0] < mundo.size and 0 <= viz[1] < mundo.size and viz not in vistos and viz not in mundo.pits:
                vistos.add(viz)
                fila.append(viz)
    return False


def venceu(mundo, cromossomo):
    """Executa a sequência numa cópia do mundo e diz se o agente venceu."""
    copia = mundo.clone()
    for acao in cromossomo:
        _, status = copia.step(acao)
        if status in ("GANHOU", "MORTO"):
            break
    return copia.won


def fitness_real(mundo, cromossomo):
    ind = Individual(0)
    ind.chromosome = list(cromossomo)
    ind.evaluate(mundo)
    return ind.fitness


class AGVariante(GeneticAlgorithm):
    """O GeneticAlgorithm do projeto, com seleção e fitness trocáveis para testar as hipóteses."""

    def __init__(self, *args, selecao="truncamento", torneio_k=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.selecao, self.torneio_k = selecao, torneio_k

    def select(self, population):
        if self.selecao == "truncamento":
            return super().select(population)
        competidores = self.rng.sample(population, min(self.torneio_k, len(population)))
        return max(competidores, key=lambda ind: ind.fitness).copia()


def busca_aleatoria(mundo, orcamento, genes, semente, **_):
    rng, melhor, melhor_f = random.Random(semente), None, None
    for _ in range(orcamento):
        c = [rng.choice(ACOES) for _ in range(genes)]
        f = fitness_real(mundo, c)
        if melhor_f is None or f > melhor_f:
            melhor, melhor_f = c, f
    return melhor, {}


def genetico(mundo, orcamento, genes, semente, populacao=40, mutacao=0.02, cruzamento=0.8, **variante):
    # A população inicial e a última geração entram no orçamento: populacao x (geracoes + 1) <= orcamento
    geracoes = max(1, orcamento // populacao - 1)
    ag = AGVariante(populacao, geracoes, genes, mutacao, cruzamento, seed=semente, **variante)
    resultado = ag.run(mundo)
    total = ag.avaliacoes + ag.acertos_cache
    return resultado["best"].chromosome, {"repetidas": ag.acertos_cache / total if total else 0.0}


def _ag(**parametros):
    return genetico, parametros


METODOS = {
    "busca_aleatoria": (busca_aleatoria, {}),
    "ag_projeto": _ag(),  # configuração atual: pais entre os 10 melhores, mutação 0,02, cruzamento 0,8
    # H1, pressão seletiva e diversidade
    "ag_torneio3": _ag(selecao="torneio", torneio_k=3),
    "ag_torneio2": _ag(selecao="torneio", torneio_k=2),
    "ag_mutacao_0.1": _ag(mutacao=0.1),
    "ag_torneio3_mut_0.1": _ag(selecao="torneio", torneio_k=3, mutacao=0.1),
    # H2, fitness sem gradiente até o ouro
    "ag_proximidade": _ag(proximidade=20.0),
    "ag_torneio3_proximidade": _ag(selecao="torneio", torneio_k=3, proximidade=20.0),
    # H4, parâmetros: população
    "ag_pop_20": _ag(populacao=20),
    "ag_pop_100": _ag(populacao=100),
    # Padrão do GeneticAgent (100 x 500 x 100), para a fase "padrao"
    "ag_padrao": _ag(populacao=100),
    "ag_padrao_mut_0.1": _ag(populacao=100, mutacao=0.1),
    "ag_padrao_proximidade": _ag(populacao=100, proximidade=20.0),
}

FASES = {
    "confirmacao": {
        "metodos": ["busca_aleatoria", "ag_projeto"],
        # (tamanho do mundo, genes, orçamento)
        "cenarios": [(n, g, b) for n in (4, 6, 8, 10, 14) for g in (40, 100) for b in (500, 2000, 10000)],
    },
    "hipoteses": {
        "metodos": [m for m in METODOS if not m.startswith("ag_padrao")],
        "cenarios": [(n, g, b) for n in (6, 10, 14) for g in (40, 100) for b in (2000,)],
    },
    # Configuração padrão do projeto: 100 indivíduos, 100 genes, 50.000 avaliações
    "padrao": {
        "metodos": ["busca_aleatoria", "ag_padrao", "ag_padrao_mut_0.1", "ag_padrao_proximidade"],
        "cenarios": [(n, 100, 50000) for n in (4, 6, 8, 10, 14)],
    },
}


def tentar(nome, mundo_n, genes, orcamento, semente):
    mundo = World(size=mundo_n, seed=semente)
    funcao, parametros = METODOS[nome]
    inicio = time.perf_counter()
    cromossomo, extra = funcao(mundo, orcamento, genes, semente, **parametros)
    return {
        "metodo": nome,
        "mundo": mundo_n,
        "genes": genes,
        "orcamento": orcamento,
        "semente": semente,
        "resolvivel": resolvivel(mundo),
        "vitoria": venceu(mundo, cromossomo),
        "fitness": fitness_real(mundo, cromossomo),
        "segundos": time.perf_counter() - inicio,
        "repetidas": extra.get("repetidas"),
    }


def holm(pvalores):
    """Correção de Holm: devolve os p-valores ajustados, na ordem original."""
    ordem = sorted(range(len(pvalores)), key=pvalores.__getitem__)
    ajustados, maior = [0.0] * len(pvalores), 0.0
    for posicao, i in enumerate(ordem):
        maior = max(maior, min(1.0, (len(pvalores) - posicao) * pvalores[i]))
        ajustados[i] = maior
    return ajustados


def comparar(tentativas):
    """Compara cada método com a busca aleatória, pareando por mundo (McNemar exato)."""
    linhas = []
    chaves = ["mundo", "genes", "orcamento"]
    for cenario, grupo in tentativas.groupby(chaves):
        pivo = grupo.pivot(index="semente", columns="metodo", values="vitoria").astype(bool)
        for metodo, base in itertools.product([m for m in pivo.columns if m != REFERENCIA], [REFERENCIA]):
            so_metodo = int((pivo[metodo] & ~pivo[base]).sum())
            so_base = int((pivo[base] & ~pivo[metodo]).sum())
            discordantes = so_metodo + so_base
            p = binomtest(so_metodo, discordantes, 0.5).pvalue if discordantes else 1.0
            linhas.append(
                {
                    **dict(zip(chaves, cenario)),
                    "metodo": metodo,
                    "vitorias_metodo": int(pivo[metodo].sum()),
                    "vitorias_aleatoria": int(pivo[base].sum()),
                    "mundos": len(pivo),
                    "so_metodo_venceu": so_metodo,
                    "so_aleatoria_venceu": so_base,
                    "p": p,
                }
            )
    df = pd.DataFrame(linhas)
    df["p_holm"] = holm(df["p"].tolist())
    return df


def main():
    parser = argparse.ArgumentParser(description="Compara métodos de busca com o mesmo orçamento de avaliações (#31)")
    parser.add_argument("--fase", choices=FASES, required=True)
    parser.add_argument("--mundos", type=int, default=100, help="Mundos por cenário (sementes 0 a N-1)")
    parser.add_argument("--saida", default=None)
    args = parser.parse_args()

    fase = FASES[args.fase]
    saida = args.saida or os.path.join("logs", f"exp31_{args.fase}_{datetime.now():%Y%m%d_%H%M%S}")
    os.makedirs(saida, exist_ok=True)
    with open(os.path.join(saida, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "versao": __version__,
                "git": estado_do_git(),
                "fase": args.fase,
                "mundos": args.mundos,
                "metodos": fase["metodos"],
                "cenarios": fase["cenarios"],
                "bibliotecas": versoes_das_bibliotecas(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    tarefas = [(m, n, g, b, s) for n, g, b in fase["cenarios"] for m in fase["metodos"] for s in range(args.mundos)]
    print(f"{len(tarefas)} tentativas em {saida}")
    inicio = time.perf_counter()
    resultados = Parallel(n_jobs=-1, batch_size="auto")(delayed(tentar)(*t) for t in tarefas)
    print(f"Concluído em {(time.perf_counter() - inicio) / 60:.1f} min")

    tentativas = pd.DataFrame(resultados)
    tentativas.to_csv(os.path.join(saida, "tentativas.csv"), index=False)
    resumo = (
        tentativas.groupby(["mundo", "genes", "orcamento", "metodo"])
        .agg(
            vitorias=("vitoria", "sum"),
            mundos=("vitoria", "size"),
            resolviveis=("resolvivel", "sum"),
            fitness_medio=("fitness", "mean"),
            repetidas_media=("repetidas", "mean"),
        )
        .reset_index()
    )
    resumo.to_csv(os.path.join(saida, "resumo.csv"), index=False)
    comparacoes = comparar(tentativas)
    comparacoes.to_csv(os.path.join(saida, "comparacoes.csv"), index=False)
    pd.set_option("display.width", 200, "display.max_rows", None)
    print(comparacoes.to_string(index=False))


if __name__ == "__main__":
    main()
