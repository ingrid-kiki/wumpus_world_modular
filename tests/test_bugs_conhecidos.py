# ==============================
# tests/test_bugs_conhecidos.py
# ==============================
'''
# Testes de caracterização dos bugs encontrados na análise do projeto (#17).
#
# Cada teste descreve o comportamento CORRETO e está marcado com xfail estrito,
# apontando a issue do bug. Enquanto o bug existir, o teste "falha como esperado".
# Quando o bug for corrigido, o teste passa e o pytest acusa XPASS(strict):
# é o sinal para remover a marcação xfail na mesma PR da correção.
'''

import random

import pytest

import benchmark
import benchmark_custom
import benchmark_fast
import benchmark_sideB
from agents.logic_knowledge_base import LogicKnowledgeBase
from ga.ga_core import GeneticAlgorithm
from ga.individual import Individual
from world.world import World

ISSUE = "https://github.com/ingrid-kiki/wumpus_world_modular/issues/"


def mundo_controlado():
    """Mundo 4x4 com posições fixas: ouro em (0,1), poço em (0,2), Wumpus em (3,3)."""
    w = World(size=4, seed=0)
    w.gold_pos = (0, 1)
    w.pits = [(0, 2)]
    w.wumpus_pos = (3, 3)
    return w


class AgenteFalso:
    """Agente que não faz nada: permite testar os benchmarks sem rodar a IA."""

    def __init__(self, world):
        self.world = world
        self.logger = None

    def run(self):
        return {"dados_extra": {"fitness": [1.0, 2.0]}}


# ---------------------------------------------------------------- Agente lógico

@pytest.mark.xfail(strict=True, reason=f"{ISSUE}18 agente lógico sai do grid e entra em loop")
def test_logico_mantem_posicao_sincronizada_com_o_mundo():
    w = World(size=4, seed=0)
    kb = LogicKnowledgeBase()
    for _ in range(5):
        acao = kb.infer_action(w.perceive())
        w.step(acao)
        kb.update_position(acao)
        assert kb.current_pos == w.agent_pos


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}18 agente lógico sai do grid e entra em loop")
def test_logico_termina_em_ate_200_passos():
    # Reproduz o laço de LogicAgent.run() com um limite, para não travar a suíte.
    w = World(size=4, seed=0)
    kb = LogicKnowledgeBase()
    passos = 0
    while not w.is_done() and passos < 200:
        acao = kb.infer_action(w.perceive())
        w.step(acao)
        kb.update_position(acao)
        passos += 1
    assert w.is_done()


# ---------------------------------------------------------------- Algoritmo genético

@pytest.mark.xfail(strict=True, reason=f"{ISSUE}19 indivíduo mutado mantém o fitness do pai")
def test_mutacao_invalida_o_fitness():
    ga = GeneticAlgorithm(pop_size=4, gens=1, chrom_length=10, mutation_rate=1.0, crossover_rate=0.0)
    ind = Individual(10)
    ind.fitness = 123.0
    ga.mutate(ind)
    assert ind.fitness is None


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}20 ouro pode ser pontuado mais de uma vez")
def test_ouro_pontua_uma_vez_so():
    w = mundo_controlado()
    uma_vez, tres_vezes = Individual(0), Individual(0)
    uma_vez.chromosome = ["DIREITA", "AGARRAR"]
    tres_vezes.chromosome = ["DIREITA", "AGARRAR", "AGARRAR", "AGARRAR"]
    uma_vez.evaluate(w)
    tres_vezes.evaluate(w)
    # Agarrar de novo não pode render outro bônus de +100.
    assert tres_vezes.fitness <= uma_vez.fitness


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}20 ações continuam tendo efeito depois da vitória")
def test_mundo_nao_muda_depois_da_vitoria():
    w = mundo_controlado()
    w.step("DIREITA")
    _, status = w.step("AGARRAR")
    assert status == "GANHOU"
    _, status = w.step("DIREITA")  # anda para o poço depois de vencer
    assert w.won and w.is_alive
    assert status == "GANHOU"


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}21 bônus de +25 por tiro nunca é concedido")
def test_tiro_com_fedor_recebe_bonus():
    w = World(size=4, seed=0)
    w.wumpus_pos = (0, 1)  # adjacente ao agente em (0,0): há FEDOR
    w.pits = [(3, 3)]
    w.gold_pos = (3, 0)
    assert "FEDOR" in w.perceive()
    ind = Individual(0)
    ind.chromosome = ["TIRO"]
    ind.evaluate(w)
    # -1 (ação) + 25 (tiro com fedor) + 10 (sobreviveu)
    assert ind.fitness == 34


# ---------------------------------------------------------------- Mundo

@pytest.mark.xfail(strict=True, reason=f"{ISSUE}22 poços podem ser sorteados na mesma casa")
def test_pocos_nao_se_sobrepoem():
    sobrepostos = [s for s in range(300) if len(set(World(size=8, seed=s).pits)) < len(World(size=8, seed=s).pits)]
    assert sobrepostos == []


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}23 World(seed=...) reinicia o gerador aleatório global")
def test_world_nao_altera_o_random_global():
    random.seed(123)
    esperado = random.random()
    random.seed(123)
    World(size=4, seed=0)
    assert random.random() == esperado


# ---------------------------------------------------------------- Benchmarks

CHAVES_RESULTADO = {"agente", "tamanho_mundo", "vitórias", "mortes", "sobreviveu", "tempo_total", "tempo_médio"}


def test_benchmark_padrao_retorna_o_contrato_do_main(monkeypatch):
    # Regressão: é o único benchmark que funciona hoje com o main.py.
    monkeypatch.setitem(benchmark.AGENTES_DISPONIVEIS, "falso", AgenteFalso)
    resultado = benchmark.executar_benchmark("falso", 4, 2)
    assert CHAVES_RESULTADO <= set(resultado)


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}24 benchmark_custom não retorna resultado")
def test_benchmark_custom_retorna_o_contrato_do_main(monkeypatch):
    monkeypatch.setitem(benchmark_custom.AGENTES_DISPONIVEIS, "falso", AgenteFalso)
    resultado = benchmark_custom.executar_benchmark("falso", 4, 2)
    assert isinstance(resultado, dict) and CHAVES_RESULTADO <= set(resultado)


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}24 benchmark_sideB não aceita num_execucoes")
def test_benchmark_sideB_aceita_a_chamada_do_main(monkeypatch):
    monkeypatch.setitem(benchmark_sideB.AGENTES_DISPONIVEIS, "falso", AgenteFalso)
    resultado = benchmark_sideB.executar_benchmark("falso", 4, 2)
    assert isinstance(resultado, dict) and CHAVES_RESULTADO <= set(resultado)


@pytest.mark.xfail(strict=True, reason=f"{ISSUE}24 benchmark_fast lê a chave errada e perde os dados extras")
def test_benchmark_fast_preserva_dados_extra():
    execucao = benchmark_fast.simular_execucao(AgenteFalso, 4, 0)
    assert execucao["dados_extra"].get("fitness") == [1.0, 2.0]
