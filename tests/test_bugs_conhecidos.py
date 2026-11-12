# ==============================
# tests/test_bugs_conhecidos.py
# ==============================
"""
# Testes dos bugs encontrados na análise do projeto (#17), issues #18 a #24.
#
# Cada teste descreve o comportamento CORRETO. Eles nasceram marcados com xfail estrito
# (Fase 2) e a marcação foi removida no commit que corrigiu cada bug (Fase 3).
# Hoje funcionam como testes de regressão: se algum voltar a falhar, o bug voltou.
#
# Para documentar um bug novo antes de corrigi-lo, use:
#     @pytest.mark.xfail(strict=True, reason=f"{ISSUE}<número> <descrição>")
"""

import random

import numpy as np
import pytest

import benchmark
import main
from agents.genetic_agent import AgenteGenetico
from agents.logic_agent import AgenteLogico
from agents.logic_knowledge_base import BaseConhecimento
from ga.ga_core import AlgoritmoGenetico
from ga.individual import Individuo
from tests.conftest import GA_RAPIDO
from world.world import Mundo

ISSUE = "https://github.com/ingrid-kiki/wumpus_world_modular/issues/"


def mundo_controlado():
    """Mundo 4x4 com posições fixas: ouro em (0,1), poço em (0,2), Wumpus em (3,3)."""
    w = Mundo(tamanho=4, semente=0)
    w.posicao_ouro = (0, 1)
    w.pocos = [(0, 2)]
    w.posicao_wumpus = (3, 3)
    return w


class AgenteFalso:
    """Agente que não faz nada: permite testar os benchmarks sem rodar a IA."""

    def __init__(self, mundo):
        self.mundo = mundo

    def executar(self):
        return {"dados_extra": {"fitness": [1.0, 2.0]}}


# ---------------------------------------------------------------- Agente lógico


def test_logico_mantem_posicao_sincronizada_com_o_mundo():
    """#18 (corrigido)."""
    w = Mundo(tamanho=4, semente=0)
    kb = BaseConhecimento(tamanho=w.tamanho)
    for _ in range(20):
        if w.terminou():
            break
        acao = kb.inferir_acao(w.perceber())
        w.agir(acao)
        kb.atualizar_posicao(acao, w.posicao_agente)
        assert kb.posicao_atual == w.posicao_agente


def test_base_nao_sai_do_mundo_mesmo_sem_a_posicao_real():
    """#18: com o tamanho conhecido, um movimento contra a parede não move a KB."""
    kb = BaseConhecimento(tamanho=4)
    kb.atualizar_posicao("CIMA")
    kb.atualizar_posicao("ESQUERDA")
    assert kb.posicao_atual == (0, 0)


@pytest.mark.parametrize("tamanho", [4, 6, 8])
def test_logico_sempre_termina(tamanho):
    """#18: em todo mundo, o agente vence, morre ou esgota o limite de passos."""
    for semente in range(30):
        w = Mundo(tamanho=tamanho, semente=semente)
        agente = AgenteLogico(w)
        resultado = agente.executar()
        assert w.terminou() or resultado["passos"] == agente.max_passos


# ---------------------------------------------------------------- Algoritmo genético


def test_mutacao_invalida_o_fitness():
    """#19 (corrigido)."""
    ag = AlgoritmoGenetico(
        tamanho_populacao=4, geracoes=1, tamanho_cromossomo=10, taxa_mutacao=1.0, taxa_cruzamento=0.0
    )
    ind = Individuo(10)
    ind.fitness = 123.0
    ag.mutar(ind)
    assert ind.fitness is None


@pytest.mark.parametrize("semente", range(5))
def test_fitness_do_melhor_individuo_corresponde_ao_cromossomo(semente):
    """#19: reavaliar o melhor indivíduo devolvido pelo AG dá o mesmo fitness (proteção contra regressão)."""
    w = Mundo(tamanho=4, semente=semente)
    ag = AlgoritmoGenetico(
        tamanho_populacao=20, geracoes=10, tamanho_cromossomo=20, taxa_mutacao=0.1, taxa_cruzamento=0.3, semente=semente
    )
    melhor = ag.executar(w)["melhor"]
    reavaliado = Individuo(0)
    reavaliado.cromossomo = list(melhor.cromossomo)
    reavaliado.avaliar(w)
    assert reavaliado.fitness == melhor.fitness


def test_ouro_pontua_uma_vez_so():
    """#20 (corrigido)."""
    w = mundo_controlado()
    uma_vez, tres_vezes = Individuo(0), Individuo(0)
    uma_vez.cromossomo = ["DIREITA", "AGARRAR"]
    tres_vezes.cromossomo = ["DIREITA", "AGARRAR", "AGARRAR", "AGARRAR"]
    uma_vez.avaliar(w)
    tres_vezes.avaliar(w)
    # Agarrar de novo não pode render outro bônus de +100: o jogo termina na vitória.
    assert tres_vezes.fitness == uma_vez.fitness


def test_mundo_nao_muda_depois_da_vitoria():
    """#20 (corrigido)."""
    w = mundo_controlado()
    w.agir("DIREITA")
    _, status = w.agir("AGARRAR")
    assert status == "GANHOU"
    _, status = w.agir("DIREITA")  # anda para o poço depois de vencer
    assert w.ganhou and w.agente_vivo
    assert status == "GANHOU"


def test_mundo_nao_muda_depois_da_morte():
    """#20: morto continua morto e parado."""
    w = mundo_controlado()
    w.posicao_ouro = (3, 0)
    w.pocos = [(0, 1)]
    _, status = w.agir("DIREITA")
    assert status == "MORTO"
    _, status = w.agir("ESQUERDA")
    assert status == "MORTO" and w.posicao_agente == (0, 1) and not w.ganhou


def test_matar_o_wumpus_recebe_bonus():
    """#21 (corrigido): +25 quando o tiro mata o Wumpus."""
    w = Mundo(tamanho=4, semente=0)
    w.posicao_wumpus = (0, 1)  # adjacente ao agente em (0,0): há FEDOR
    w.pocos = [(3, 3)]
    w.posicao_ouro = (3, 0)
    assert "FEDOR" in w.perceber()
    ind = Individuo(0)
    ind.cromossomo = ["TIRO"]
    ind.avaliar(w)
    # -1 (ação) + 25 (matou o Wumpus) + 10 (sobreviveu)
    assert ind.fitness == 34


def test_tiro_sem_acertar_nao_recebe_bonus():
    """#21: errar o tiro (ou atirar com o Wumpus já morto) custa só a ação."""
    w = Mundo(tamanho=4, semente=0)
    w.posicao_wumpus = (3, 3)  # longe do agente
    w.pocos = [(2, 2)]
    w.posicao_ouro = (3, 0)
    ind = Individuo(0)
    ind.cromossomo = ["TIRO"]
    ind.avaliar(w)
    assert ind.fitness == 9  # -1 + 10
    w.posicao_wumpus = (0, 1)
    ind.cromossomo = ["TIRO", "TIRO"]
    ind.avaliar(w)
    assert ind.fitness == 33  # -1 + 25, depois -1, + 10


# ---------------------------------------------------------------- Mundo


def test_pocos_nao_se_sobrepoem():
    """#22 (corrigido)."""
    for tamanho in (4, 6, 8):
        for semente in range(300):
            w = Mundo(tamanho=tamanho, semente=semente)
            assert len(set(w.pocos)) == len(w.pocos) == tamanho // 2
            assert not {w.posicao_agente, w.posicao_ouro, w.posicao_wumpus} & set(w.pocos)


def test_mundo_nao_altera_o_random_global():
    """#23 (corrigido)."""
    random.seed(123)
    esperado = random.random()
    random.seed(123)
    Mundo(tamanho=4, semente=0)
    assert random.random() == esperado


def test_mesma_semente_gera_o_mesmo_mundo():
    a, b = Mundo(tamanho=6, semente=7), Mundo(tamanho=6, semente=7)
    assert (a.posicao_ouro, a.posicao_wumpus, a.pocos) == (b.posicao_ouro, b.posicao_wumpus, b.pocos)


def test_ag_reprodutivel_com_a_semente_do_mundo():
    """#23: o AG usa a semente do mundo e não depende do random global."""
    resultados = []
    for lixo in (1, 2):
        random.seed(lixo)  # estado global diferente a cada rodada
        agente = AgenteGenetico(Mundo(tamanho=4, semente=3), **GA_RAPIDO)
        r = agente.executar()
        resultados.append([passo["acao"] for passo in r["historico"]])
    assert resultados[0] == resultados[1]


# ---------------------------------------------------------------- Benchmarks

CHAVES_RESULTADO = {
    "agente",
    "tamanho_mundo",
    "vitorias",
    "mortes",
    "sobreviveu",
    "erros",
    "tempo_total",
    "tempo_medio",
    "dados_extra",
}

# O benchmark único tem dois modos; antes eram cinco arquivos com o mesmo contrato
MODOS = {"sequencial": False, "paralelo": True}


def _paralelo_sequencial(n_jobs=None):
    """Substitui joblib.Parallel nos testes: roda as tarefas em sequência, no mesmo processo."""
    return lambda tarefas: [funcao(*args, **kwargs) for funcao, args, kwargs in tarefas]


def _rodar(modo, monkeypatch, classe_agente, execucoes):
    monkeypatch.setitem(benchmark.AGENTES_DISPONIVEIS, "falso", classe_agente)
    monkeypatch.setattr(benchmark, "Parallel", _paralelo_sequencial)
    return benchmark.executar_benchmark("falso", 4, execucoes, paralelo=MODOS[modo])


class AgenteQueFalha(AgenteFalso):
    """Falha na execução com semente 1; as outras terminam normalmente."""

    def executar(self):
        if self.mundo.semente == 1:
            raise RuntimeError("falha de propósito")
        return super().executar()


@pytest.mark.parametrize("modo", MODOS)
def test_benchmarks_cumprem_o_contrato_do_main(modo, monkeypatch):
    """#24 (corrigido): os 5 benchmarks aceitam (agente, tamanho, execuções) e devolvem o mesmo dict."""
    resultado = _rodar(modo, monkeypatch, AgenteFalso, 2)
    assert isinstance(resultado, dict) and set(resultado) >= CHAVES_RESULTADO
    assert resultado["vitorias"] + resultado["mortes"] + resultado["sobreviveu"] == 2
    assert resultado["erros"] == 0
    assert resultado["dados_extra"] == {"fitness": [1.0, 2.0]}


@pytest.mark.parametrize("modo", MODOS)
def test_erro_nao_vira_resultado_nem_derruba_o_benchmark(modo, monkeypatch, capsys):
    """#30: a execução que falha entra em 'erros'; as outras continuam e o traceback vai para o stderr."""
    resultado = _rodar(modo, monkeypatch, AgenteQueFalha, 3)
    assert resultado["erros"] == 1
    assert resultado["vitorias"] + resultado["mortes"] + resultado["sobreviveu"] == 2
    assert resultado["dados_extra"] == {"fitness": [1.0, 2.0]}
    assert "RuntimeError: falha de propósito" in capsys.readouterr().err


@pytest.mark.parametrize("modo", MODOS)
def test_dados_extra_vem_da_primeira_execucao_sem_erro(modo, monkeypatch):
    """#30: se a primeira execução falha, os dados extras vêm da seguinte."""

    class FalhaNaPrimeira(AgenteFalso):
        def executar(self):
            if self.mundo.semente == 0:
                raise RuntimeError("falha de propósito")
            return super().executar()

    resultado = _rodar(modo, monkeypatch, FalhaNaPrimeira, 2)
    assert resultado["erros"] == 1 and resultado["dados_extra"] == {"fitness": [1.0, 2.0]}


def test_saida_do_terminal_inclui_o_stderr():
    """#30: tracebacks e avisos (stderr) também vão para o saida_terminal.txt."""
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
    saida = subprocess.run(
        [sys.executable, "benchmark.py"],
        cwd=raiz,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"},
    )
    assert saida.returncode == 0, saida.stderr[-2000:]
    assert "Resumo para manual" not in saida.stdout
    assert "Resumo para logico" in saida.stdout and "Resumo para genetico" in saida.stdout
    assert "EOF when reading a line" not in saida.stdout + saida.stderr


def test_simular_execucao_preserva_dados_extra():
    """#24 (corrigido)."""
    execucao = benchmark.simular_execucao(AgenteFalso, 4, 0)
    assert execucao["dados_extra"].get("fitness") == [1.0, 2.0]


def test_csv_do_main_so_tem_colunas_escalares(tmp_path):
    """#24: dados_extra sai do CSV e vai para um .npz por agente e tamanho."""
    resultados = [
        {
            "agente": "genetico",
            "tamanho_mundo": 4,
            "vitorias": 1,
            "mortes": 0,
            "sobreviveu": 0,
            "tempo_total": 1.0,
            "tempo_medio": 1.0,
            "dados_extra": {"fitness": [1.0, 2.0], "cpu": [3.0]},
        },
        {
            "agente": "logico",
            "tamanho_mundo": 4,
            "vitorias": 0,
            "mortes": 1,
            "sobreviveu": 0,
            "tempo_total": 0.1,
            "tempo_medio": 0.1,
            "dados_extra": {},
        },
        None,  # benchmark que falhou não derruba a gravação
    ]
    df, caminho_csv = main.salvar_resultados(resultados, str(tmp_path))
    assert "dados_extra" not in df.columns and len(df) == 2
    with open(caminho_csv, encoding="utf-8") as csv:
        assert "..." not in csv.read()
    dados = np.load(tmp_path / "dados_extra_genetico_4x4.npz")
    assert list(dados["fitness"]) == [1.0, 2.0]
    assert not (tmp_path / "dados_extra_logico_4x4.npz").exists()


def test_traceback_do_modo_paralelo_chega_a_saida_do_terminal(tmp_path, monkeypatch):
    """#40: com processos paralelos de verdade, o erro aparece uma vez no saida_terminal.txt."""
    monkeypatch.setitem(benchmark.AGENTES_DISPONIVEIS, "falso", AgenteQueFalha)
    caminho = tmp_path / "saida_terminal.txt"
    with main.capturar_saida_terminal(str(caminho)):
        resultado = benchmark.executar_benchmark("falso", 4, 3, paralelo=True)
    assert resultado["erros"] == 1
    log = caminho.read_text(encoding="utf-8")
    assert log.count("RuntimeError: falha de propósito") == 2  # a linha do resumo e a do traceback
    assert "Traceback (most recent call last)" in log


@pytest.mark.parametrize(
    "linha, windows, esperado",
    [
        (r"--saida logs\teste --tamanhos 4", True, ["--saida", r"logs\teste", "--tamanhos", "4"]),
        (r"--saida C:\Users\ana\run", True, ["--saida", r"C:\Users\ana\run"]),
        (r'--saida "C:\Minha Pasta\run"', True, ["--saida", r"C:\Minha Pasta\run"]),
        ("--saida logs/teste", True, ["--saida", "logs/teste"]),
        ('--saida "minha pasta/run"', False, ["--saida", "minha pasta/run"]),
        (
            "--agentes logico genetico --tamanhos 4 6",
            False,
            ["--agentes", "logico", "genetico", "--tamanhos", "4", "6"],
        ),
    ],
    ids=["relativo", "absoluto", "com_espaco_e_aspas", "barra_normal", "linux_aspas", "sem_caminho"],
)
def test_opcao_5_preserva_caminhos(linha, windows, esperado):
    """#39: o shlex apagava as barras invertidas de caminhos do Windows."""
    assert main.separar_argumentos(linha, windows=windows) == esperado
