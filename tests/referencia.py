# ==============================
# tests/referencia.py
# ==============================
"""
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
"""

import contextlib
import hashlib
import io
import json
import pathlib

from agents.genetic_agent import AgenteGenetico
from agents.logic_agent import AgenteLogico
from agents.logic_knowledge_base import BaseConhecimento
from agents.random_search_agent import AgenteAleatorio
from ga.individual import Individuo
from utils.execucao import classificar
from world.world import Mundo

ARQUIVO = pathlib.Path(__file__).with_name("referencia.json")
TAMANHOS = (4, 6, 8)
SEMENTES = range(5)
SEMENTES_LOGICO = range(40)
AG_RAPIDO = {"tamanho_populacao": 20, "geracoes": 10, "tamanho_cromossomo": 20}

AGENTES = {
    "logico": (AgenteLogico, {}),
    "genetico": (AgenteGenetico, AG_RAPIDO),
    "genetico_proximidade": (AgenteGenetico, {**AG_RAPIDO, "proximidade": 20.0}),
    "aleatorio": (AgenteAleatorio, {"avaliacoes": 200, "tamanho_cromossomo": 20}),
}


def _resumo_do_historico(historico):
    """Hash curto do histórico: muda se qualquer ação ou percepção mudar."""
    texto = json.dumps(historico, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def _fitness_das_acoes(historico, tamanho, semente, proximidade=0.0):
    """Fitness da sequência executada: acusa mudanças nos pontos, mesmo sem mudar o melhor indivíduo."""
    acoes = [passo["acao"] for passo in historico]
    if not acoes:
        return None
    individuo = Individuo(0)
    individuo.cromossomo = acoes
    individuo.avaliar(Mundo(tamanho=tamanho, semente=semente), proximidade)
    return individuo.fitness


def _casos_de_fitness():
    """Sequências escritas à mão para exercitar cada regra do fitness, inclusive matar o Wumpus."""
    mundo = Mundo(tamanho=5, semente=0)
    mundo.posicao_ouro, mundo.pocos, mundo.posicao_wumpus = (0, 2), [(2, 0)], (1, 1)
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
            individuo = Individuo(0)
            individuo.cromossomo = cromossomo
            individuo.avaliar(mundo, proximidade)
            resultado[f"{nome}|proximidade={proximidade:g}"] = individuo.fitness
    return resultado


def _casos_do_agente_logico():
    """Decisões raras em jogo real: com as vizinhas já visitadas, volta pela menos visitada."""

    def decidir(posicao, visitas):
        base = BaseConhecimento(tamanho=3)
        base.posicao_atual = posicao
        base.conhecidas = {casa: {"seguro": True, "visitado": True, "percepcoes": []} for casa in visitas}
        base.visitas = dict(visitas)
        return base.inferir_acao([])

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
            m = Mundo(tamanho=tamanho, semente=semente)
            mundos.append(
                {
                    "tamanho": tamanho,
                    "semente": semente,
                    "ouro": list(m.posicao_ouro),
                    "wumpus": list(m.posicao_wumpus),
                    "pocos": [list(p) for p in m.pocos],
                }
            )
        for nome, (classe, parametros) in AGENTES.items():
            # O agente lógico é instantâneo: mais mundos para alcançar todos os caminhos da decisão
            for semente in SEMENTES_LOGICO if nome == "logico" else SEMENTES:
                mundo = Mundo(tamanho=tamanho, semente=semente)
                with contextlib.redirect_stdout(io.StringIO()):
                    resultado = classe(mundo, **parametros).executar()
                historico = resultado["historico"]
                execucoes.append(
                    {
                        "agente": nome,
                        "tamanho": tamanho,
                        "semente": semente,
                        "status": classificar(mundo),
                        "passos": len(historico),
                        "fitness": _fitness_das_acoes(historico, tamanho, semente, parametros.get("proximidade", 0.0)),
                        "historico": _resumo_do_historico(historico),
                    }
                )
    return {
        "mundos": mundos,
        "execucoes": execucoes,
        "casos_de_fitness": _casos_de_fitness(),
        "casos_do_agente_logico": _casos_do_agente_logico(),
    }


if __name__ == "__main__":
    ARQUIVO.write_text(json.dumps(calcular(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"Referência atualizada em {ARQUIVO}")
