# ==============================
# tests/referencia.py
# ==============================
'''
# Cenário de referência do projeto: um conjunto fixo de mundos e agentes cujos resultados não
# podem mudar sem uma decisão explícita. É o que protege as etapas de limpeza e refatoração.
#
# O teste em tests/test_referencia.py compara o resultado atual com tests/referencia.json.
# Compara números e sequências de ações, nunca imagens: os PNGs mudam entre Windows e Linux.
#
# Se uma mudança nos resultados for INTENCIONAL (por exemplo, uma alteração decidida no método),
# regenere o arquivo e explique o motivo no commit e no CHANGELOG:
#
#     python -m tests.referencia
'''

import contextlib
import hashlib
import io
import json
import pathlib

from agents.genetic_agent import GeneticAgent
from agents.logic_agent import LogicAgent
from agents.logic_knowledge_base import LogicKnowledgeBase
from agents.random_search_agent import RandomSearchAgent
from ga.individual import Individual
from utils.execucao import classificar
from world.world import World

ARQUIVO = pathlib.Path(__file__).with_name("referencia.json")
TAMANHOS = (4, 6, 8)
SEMENTES = range(5)
SEMENTES_LOGICO = range(40)
AG_RAPIDO = {"population_size": 20, "gens": 10, "chrom_length": 20}

AGENTES = {
    "logico": (LogicAgent, {}),
    "genetico": (GeneticAgent, AG_RAPIDO),
    "genetico_proximidade": (GeneticAgent, {**AG_RAPIDO, "proximidade": 20.0}),
    "aleatorio": (RandomSearchAgent, {"avaliacoes": 200, "chrom_length": 20}),
}


def _resumo_do_historico(historico):
    """Hash curto do histórico: muda se qualquer ação ou percepção mudar."""
    texto = json.dumps(historico, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def _fitness_das_acoes(historico, tamanho, semente, proximidade=0.0):
    """Fitness da sequência executada: acusa mudanças nos pontos, mesmo sem mudar o melhor indivíduo."""
    acoes = [passo["ação"] for passo in historico if "ação" in passo]
    if not acoes:
        return None  # o agente lógico não registra as ações
    individuo = Individual(0)
    individuo.chromosome = acoes
    individuo.evaluate(World(size=tamanho, seed=semente), proximidade)
    return individuo.fitness


def _casos_de_fitness():
    """Sequências escritas à mão para exercitar cada regra do fitness, inclusive matar o Wumpus."""
    mundo = World(size=5, seed=0)
    mundo.gold_pos, mundo.pits, mundo.wumpus_pos = (0, 2), [(2, 0)], (1, 1)
    casos = {
        "andar": ["DIREITA"],
        "contra_a_parede": ["CIMA", "ESQUERDA"],
        "agarrar_sem_ouro": ["AGARRAR"],
        "tiro_errado": ["TIRO"],
        "matar_wumpus": ["DIREITA", "TIRO"],
        "pegar_o_ouro": ["DIREITA", "DIREITA", "AGARRAR"],
        "cair_no_poco": ["BAIXO", "BAIXO"],
        "morrer_para_o_wumpus": ["DIREITA", "BAIXO"],
    }
    resultado = {}
    for nome, cromossomo in casos.items():
        for proximidade in (0.0, 20.0):
            individuo = Individual(0)
            individuo.chromosome = cromossomo
            individuo.evaluate(mundo, proximidade)
            resultado[f"{nome}|proximidade={proximidade:g}"] = individuo.fitness
    return resultado


def _casos_do_agente_logico():
    """Decisões raras em jogo real: com as vizinhas já visitadas, volta pela menos visitada."""
    def decidir(posicao, visitas):
        base = LogicKnowledgeBase(size=3)
        base.current_pos = posicao
        base.known = {casa: {"seguro": True, "visitado": True, "percepções": []} for casa in visitas}
        base.visits = dict(visitas)
        return base.infer_action([])

    return {
        "desempate_pela_ordem_dos_movimentos": decidir((1, 1), {(0, 1): 1, (2, 1): 1, (1, 0): 1, (1, 2): 1}),
        "volta_pela_menos_visitada_baixo": decidir((1, 1), {(0, 1): 3, (2, 1): 1, (1, 0): 2, (1, 2): 2}),
        "volta_pela_menos_visitada_esquerda": decidir((1, 1), {(0, 1): 3, (2, 1): 3, (1, 0): 1, (1, 2): 2}),
        "canto_inferior_direito": decidir((2, 2), {(1, 2): 2, (2, 1): 1}),
    }


def calcular():
    """Roda o cenário de referência e devolve um dicionário só com valores comparáveis."""
    mundos, execucoes = [], []
    for tamanho in TAMANHOS:
        for semente in SEMENTES:
            m = World(size=tamanho, seed=semente)
            mundos.append({"tamanho": tamanho, "semente": semente, "ouro": list(m.gold_pos),
                           "wumpus": list(m.wumpus_pos), "pocos": [list(p) for p in m.pits]})
        for nome, (classe, parametros) in AGENTES.items():
            # O agente lógico é instantâneo: mais mundos para alcançar todos os caminhos da decisão
            for semente in (SEMENTES_LOGICO if nome == "logico" else SEMENTES):
                mundo = World(size=tamanho, seed=semente)
                with contextlib.redirect_stdout(io.StringIO()):
                    resultado = classe(mundo, **parametros).run()
                historico = resultado["history"]
                execucoes.append({"agente": nome, "tamanho": tamanho, "semente": semente,
                                  "status": classificar(mundo), "passos": len(historico),
                                  "fitness": _fitness_das_acoes(historico, tamanho, semente,
                                                                parametros.get("proximidade", 0.0)),
                                  "historico": _resumo_do_historico(historico)})
    return {"mundos": mundos, "execucoes": execucoes, "casos_de_fitness": _casos_de_fitness(),
            "casos_do_agente_logico": _casos_do_agente_logico()}


if __name__ == "__main__":
    ARQUIVO.write_text(json.dumps(calcular(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"Referência atualizada em {ARQUIVO}")
