# ==============================
# tests/test_bugs_conhecidos.py
# ==============================
'''
# Testes dos bugs encontrados na análise do projeto (#17), issues #18 a #24.
#
# Cada teste descreve o comportamento CORRETO. Eles nasceram marcados com xfail estrito
# (Fase 2) e a marcação foi removida no commit que corrigiu cada bug (Fase 3).
# Hoje funcionam como testes de regressão: se algum voltar a falhar, o bug voltou.
#
# Para documentar um bug novo antes de corrigi-lo, use:
#     @pytest.mark.xfail(strict=True, reason=f"{ISSUE}<número> <descrição>")
'''

import random

import numpy as np
import pytest

import benchmark
import benchmark_custom
import benchmark_fast
import benchmark_graficos
import benchmark_sideB
import main
from agents.logic_agent import LogicAgent
from agents.logic_knowledge_base import LogicKnowledgeBase
from ga.ga_core import GeneticAlgorithm
from agents.genetic_agent import GeneticAgent
from ga.individual import Individual
from world.world import World
from tests.conftest import GA_RAPIDO

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

def test_logico_mantem_posicao_sincronizada_com_o_mundo():
    """#18 (corrigido)."""
    w = World(size=4, seed=0)
    kb = LogicKnowledgeBase(size=w.size)
    for _ in range(20):
        if w.is_done():
            break
        acao = kb.infer_action(w.perceive())
        w.step(acao)
        kb.update_position(acao, w.agent_pos)
        assert kb.current_pos == w.agent_pos


def test_kb_nao_sai_do_grid_mesmo_sem_a_posicao_do_mundo():
    """#18: com o tamanho conhecido, um movimento contra a parede não move a KB."""
    kb = LogicKnowledgeBase(size=4)
    kb.update_position("CIMA")
    kb.update_position("ESQUERDA")
    assert kb.current_pos == (0, 0)


@pytest.mark.parametrize("tamanho", [4, 6, 8])
def test_logico_sempre_termina(tamanho):
    """#18: em todo mundo, o agente vence, morre ou esgota o limite de passos."""
    for semente in range(30):
        w = World(size=tamanho, seed=semente)
        agente = LogicAgent(w)
        resultado = agente.run()
        assert w.is_done() or resultado["passos"] == agente.max_steps


# ---------------------------------------------------------------- Algoritmo genético

def test_mutacao_invalida_o_fitness():
    """#19 (corrigido)."""
    ga = GeneticAlgorithm(pop_size=4, gens=1, chrom_length=10, mutation_rate=1.0, crossover_rate=0.0)
    ind = Individual(10)
    ind.fitness = 123.0
    ga.mutate(ind)
    assert ind.fitness is None



@pytest.mark.parametrize("semente", range(5))
def test_fitness_do_melhor_individuo_corresponde_ao_cromossomo(semente):
    """#19: reavaliar o melhor indivíduo devolvido pelo AG dá o mesmo fitness (proteção contra regressão)."""
    w = World(size=4, seed=semente)
    ga = GeneticAlgorithm(pop_size=20, gens=10, chrom_length=20, mutation_rate=0.1, crossover_rate=0.3, seed=semente)
    melhor = ga.run(w)["best"]
    reavaliado = Individual(0)
    reavaliado.chromosome = list(melhor.chromosome)
    reavaliado.evaluate(w)
    assert reavaliado.fitness == melhor.fitness

def test_ouro_pontua_uma_vez_so():
    """#20 (corrigido)."""
    w = mundo_controlado()
    uma_vez, tres_vezes = Individual(0), Individual(0)
    uma_vez.chromosome = ["DIREITA", "AGARRAR"]
    tres_vezes.chromosome = ["DIREITA", "AGARRAR", "AGARRAR", "AGARRAR"]
    uma_vez.evaluate(w)
    tres_vezes.evaluate(w)
    # Agarrar de novo não pode render outro bônus de +100: o jogo termina na vitória.
    assert tres_vezes.fitness == uma_vez.fitness


def test_mundo_nao_muda_depois_da_vitoria():
    """#20 (corrigido)."""
    w = mundo_controlado()
    w.step("DIREITA")
    _, status = w.step("AGARRAR")
    assert status == "GANHOU"
    _, status = w.step("DIREITA")  # anda para o poço depois de vencer
    assert w.won and w.is_alive
    assert status == "GANHOU"



def test_mundo_nao_muda_depois_da_morte():
    """#20: morto continua morto e parado."""
    w = mundo_controlado()
    w.gold_pos = (3, 0)
    w.pits = [(0, 1)]
    _, status = w.step("DIREITA")
    assert status == "MORTO"
    _, status = w.step("ESQUERDA")
    assert status == "MORTO" and w.agent_pos == (0, 1) and not w.won

def test_matar_o_wumpus_recebe_bonus():
    """#21 (corrigido): +25 quando o tiro mata o Wumpus."""
    w = World(size=4, seed=0)
    w.wumpus_pos = (0, 1)  # adjacente ao agente em (0,0): há FEDOR
    w.pits = [(3, 3)]
    w.gold_pos = (3, 0)
    assert "FEDOR" in w.perceive()
    ind = Individual(0)
    ind.chromosome = ["TIRO"]
    ind.evaluate(w)
    # -1 (ação) + 25 (matou o Wumpus) + 10 (sobreviveu)
    assert ind.fitness == 34


def test_tiro_sem_acertar_nao_recebe_bonus():
    """#21: errar o tiro (ou atirar com o Wumpus já morto) custa só a ação."""
    w = World(size=4, seed=0)
    w.wumpus_pos = (3, 3)  # longe do agente
    w.pits = [(2, 2)]
    w.gold_pos = (3, 0)
    ind = Individual(0)
    ind.chromosome = ["TIRO"]
    ind.evaluate(w)
    assert ind.fitness == 9  # -1 + 10
    w.wumpus_pos = (0, 1)
    ind.chromosome = ["TIRO", "TIRO"]
    ind.evaluate(w)
    assert ind.fitness == 33  # -1 + 25, depois -1, + 10


# ---------------------------------------------------------------- Mundo

def test_pocos_nao_se_sobrepoem():
    """#22 (corrigido)."""
    for tamanho in (4, 6, 8):
        for semente in range(300):
            w = World(size=tamanho, seed=semente)
            assert len(set(w.pits)) == len(w.pits) == tamanho // 2
            assert not {w.agent_pos, w.gold_pos, w.wumpus_pos} & set(w.pits)


def test_world_nao_altera_o_random_global():
    """#23 (corrigido)."""
    random.seed(123)
    esperado = random.random()
    random.seed(123)
    World(size=4, seed=0)
    assert random.random() == esperado



def test_mesma_semente_gera_o_mesmo_mundo():
    a, b = World(size=6, seed=7), World(size=6, seed=7)
    assert (a.gold_pos, a.wumpus_pos, a.pits) == (b.gold_pos, b.wumpus_pos, b.pits)


def test_ag_reprodutivel_com_a_semente_do_mundo():
    """#23: o AG usa a semente do mundo e não depende do random global."""
    resultados = []
    for lixo in (1, 2):
        random.seed(lixo)  # estado global diferente a cada rodada
        agente = GeneticAgent(World(size=4, seed=3), **GA_RAPIDO)
        r = agente.run()
        resultados.append([passo["ação"] for passo in r["history"]])
    assert resultados[0] == resultados[1]

# ---------------------------------------------------------------- Benchmarks

CHAVES_RESULTADO = {"agente", "tamanho_mundo", "vitórias", "mortes", "sobreviveu", "erros", "tempo_total",
                    "tempo_médio", "dados_extra"}

BENCHMARKS = [benchmark, benchmark_custom, benchmark_sideB, benchmark_fast, benchmark_graficos]


def _paralelo_sequencial(n_jobs=None):
    """Substitui joblib.Parallel nos testes: roda as tarefas em sequência, no mesmo processo."""
    return lambda tarefas: [funcao(*args, **kwargs) for funcao, args, kwargs in tarefas]


def _rodar(modulo, monkeypatch, agente_cls, execucoes):
    monkeypatch.setitem(modulo.AGENTES_DISPONIVEIS, "falso", agente_cls)
    if hasattr(modulo, "Parallel"):
        monkeypatch.setattr(modulo, "Parallel", _paralelo_sequencial)
    return modulo.executar_benchmark("falso", 4, execucoes)


class AgenteQueFalha(AgenteFalso):
    """Falha na execução com semente 1; as outras terminam normalmente."""

    def run(self):
        if self.world.seed == 1:
            raise RuntimeError("falha de propósito")
        return super().run()


@pytest.mark.parametrize("modulo", BENCHMARKS, ids=lambda m: m.__name__)
def test_benchmarks_cumprem_o_contrato_do_main(modulo, monkeypatch):
    """#24 (corrigido): os 5 benchmarks aceitam (agente, tamanho, execuções) e devolvem o mesmo dict."""
    resultado = _rodar(modulo, monkeypatch, AgenteFalso, 2)
    assert isinstance(resultado, dict) and CHAVES_RESULTADO <= set(resultado)
    assert resultado["vitórias"] + resultado["mortes"] + resultado["sobreviveu"] == 2
    assert resultado["erros"] == 0
    assert resultado["dados_extra"] == {"fitness": [1.0, 2.0]}


@pytest.mark.parametrize("modulo", BENCHMARKS, ids=lambda m: m.__name__)
def test_erro_nao_vira_resultado_nem_derruba_o_benchmark(modulo, monkeypatch, capsys):
    """#30: a execução que falha entra em 'erros'; as outras continuam e o traceback vai para o stderr."""
    resultado = _rodar(modulo, monkeypatch, AgenteQueFalha, 3)
    assert resultado["erros"] == 1
    assert resultado["vitórias"] + resultado["mortes"] + resultado["sobreviveu"] == 2
    assert resultado["dados_extra"] == {"fitness": [1.0, 2.0]}
    assert "RuntimeError: falha de propósito" in capsys.readouterr().err


@pytest.mark.parametrize("modulo", BENCHMARKS, ids=lambda m: m.__name__)
def test_dados_extra_vem_da_primeira_execucao_sem_erro(modulo, monkeypatch):
    """#30: se a primeira execução falha, os dados extras vêm da seguinte."""
    class FalhaNaPrimeira(AgenteFalso):
        def run(self):
            if self.world.seed == 0:
                raise RuntimeError("falha de propósito")
            return super().run()

    resultado = _rodar(modulo, monkeypatch, FalhaNaPrimeira, 2)
    assert resultado["erros"] == 1 and resultado["dados_extra"] == {"fitness": [1.0, 2.0]}


def test_terminal_output_inclui_o_stderr():
    """#30: tracebacks e avisos (stderr) também vão para o terminal_output.txt."""
    import sys
    stdout_antes, stderr_antes = sys.stdout, sys.stderr
    with main.capturar_saida_terminal() as buffer:
        print("linha do stdout")
        print("linha do stderr", file=sys.stderr)
    texto = buffer.getvalue()
    assert "linha do stdout" in texto and "linha do stderr" in texto
    assert sys.stdout is stdout_antes and sys.stderr is stderr_antes  # restaurados ao sair


def test_benchmark_py_sozinho_nao_roda_o_agente_manual():
    """#30: 'python benchmark.py' só testa agentes automáticos; antes o manual falhava 3 vezes sem teclado."""
    import os
    import subprocess
    import sys
    raiz = os.path.dirname(os.path.abspath(benchmark.__file__))
    saida = subprocess.run([sys.executable, "benchmark.py"], cwd=raiz, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, encoding="utf-8", timeout=180,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"})
    assert saida.returncode == 0, saida.stderr[-2000:]
    assert "Resumo para manual" not in saida.stdout
    assert "Resumo para logico" in saida.stdout and "Resumo para genetico" in saida.stdout
    assert "EOF when reading a line" not in saida.stdout + saida.stderr


def test_benchmark_fast_preserva_dados_extra():
    """#24 (corrigido)."""
    execucao = benchmark_fast.simular_execucao(AgenteFalso, 4, 0)
    assert execucao["dados_extra"].get("fitness") == [1.0, 2.0]


def test_csv_do_main_so_tem_colunas_escalares(tmp_path):
    """#24: dados_extra sai do CSV e vai para um .npz por agente e tamanho."""
    resultados = [
        {"agente": "genetico", "tamanho_mundo": 4, "vitórias": 1, "mortes": 0, "sobreviveu": 0,
         "tempo_total": 1.0, "tempo_médio": 1.0, "dados_extra": {"fitness": [1.0, 2.0], "cpu": [3.0]}},
        {"agente": "logico", "tamanho_mundo": 4, "vitórias": 0, "mortes": 1, "sobreviveu": 0,
         "tempo_total": 0.1, "tempo_médio": 0.1, "dados_extra": {}},
        None,  # benchmark que falhou não derruba a gravação
    ]
    df, csv_path = main.salvar_resultados(resultados, str(tmp_path))
    assert "dados_extra" not in df.columns and len(df) == 2
    assert "..." not in open(csv_path, encoding="utf-8").read()
    dados = np.load(tmp_path / "dados_extra_genetico_4x4.npz")
    assert list(dados["fitness"]) == [1.0, 2.0]
    assert not (tmp_path / "dados_extra_logico_4x4.npz").exists()
