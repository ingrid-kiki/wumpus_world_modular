# ==============================
# tests/test_entradas.py
# ==============================
"""
# Testes de #38: entradas inválidas têm mensagem clara e nunca travam o programa.
"""

import builtins

import pytest

import main
from world.world import World


@pytest.mark.parametrize("tamanho", [1, 0, -3])
def test_mundo_rejeita_tamanho_invalido(tamanho):
    """Antes, tamanho 1 entrava em loop infinito em random_pos()."""
    with pytest.raises(ValueError, match="tamanho 2 ou maior"):
        World(size=tamanho, seed=0)


def test_menor_mundo_valido_funciona():
    w = World(size=2, seed=0)
    assert {w.agent_pos, w.gold_pos, w.wumpus_pos, *w.pits} == {(0, 0), (0, 1), (1, 0), (1, 1)}


@pytest.mark.parametrize(
    "args, trecho",
    [
        (["--execucoes", "0"], "precisa ser 1 ou maior"),
        (["--execucoes", "-1"], "precisa ser 1 ou maior"),
        (["--execucoes", "abc"], "não é um número inteiro"),
        (["--sizes", "1"], "precisa ser 2 ou maior"),
        (["--sizes", "0"], "precisa ser 2 ou maior"),
        (["--populacao", "0"], "precisa ser 1 ou maior"),
        (["--geracoes", "-1"], "precisa ser 0 ou maior"),
        (["--cromossomo", "0"], "precisa ser 1 ou maior"),
        (["--mutacao", "5"], "entre 0 e 1"),
        (["--cruzamento", "-0.1"], "entre 0 e 1"),
        (["--mutacao", "x"], "não é um número"),
        (["--agentes", "manual"], "manual"),
        (["--benchmark", "nao_existe.py"], "arquivo não encontrado"),
    ],
)
def test_opcao_invalida_tem_mensagem_clara(args, trecho, capsys):
    with pytest.raises(SystemExit) as saida:
        main.criar_parser().parse_args(args)
    assert saida.value.code == 2
    erro = capsys.readouterr().err
    assert trecho in erro and "Traceback" not in erro


def test_opcoes_validas_nos_limites():
    args = main.criar_parser().parse_args(
        [
            "--execucoes",
            "1",
            "--sizes",
            "2",
            "--populacao",
            "1",
            "--geracoes",
            "0",
            "--cromossomo",
            "1",
            "--mutacao",
            "0",
            "--cruzamento",
            "1",
        ]
    )
    assert args.execucoes == 1 and args.sizes == [2]
    assert main.parametros_do_ag(args) == {
        "population_size": 1,
        "gens": 0,
        "chrom_length": 1,
        "mutation_rate": 0.0,
        "crossover_rate": 1.0,
    }


def test_opcoes_padrao_continuam_validas():
    args = main.criar_parser().parse_args([])
    assert args.execucoes == 32 and args.sizes == [4, 6, 8] and args.benchmark == "benchmark.py"
    assert args.agentes == ["logico", "genetico"]


def respostas(monkeypatch, *valores):
    fila = iter(valores)
    monkeypatch.setattr(builtins, "input", lambda pergunta="": next(fila))


def test_menu_repete_ate_receber_tamanho_valido(monkeypatch, capsys):
    respostas(monkeypatch, "abc", "1", "4")
    assert main.perguntar_inteiro("Tamanho: ", minimo=2) == 4
    saida = capsys.readouterr().out
    assert "não é um número inteiro" in saida and "2 ou maior" in saida


def test_semente_em_branco_e_opcional(monkeypatch):
    respostas(monkeypatch, "")
    assert main.perguntar_inteiro("Semente: ", opcional=True) is None


def test_semente_invalida_pergunta_de_novo(monkeypatch):
    respostas(monkeypatch, "xyz", "7")
    assert main.perguntar_inteiro("Semente: ", opcional=True) == 7


def test_execucao_unica_termina_com_entradas_corrigidas(monkeypatch, capsys):
    """Tamanho 1 no menu travava o programa."""
    respostas(monkeypatch, "1", "abc", "4", "3")
    main.execucao_unica("logico")
    assert "mundo 4x4" in capsys.readouterr().out


def test_cromossomo_de_um_gene_nao_gera_erro(tmp_path):
    """Com um gene só, o cruzamento falhava e toda execução virava erro."""
    pasta = tmp_path / "run"
    _, df = main.rodar_benchmark(
        [
            "--agentes",
            "genetico",
            "--sizes",
            "4",
            "--execucoes",
            "2",
            "--populacao",
            "10",
            "--geracoes",
            "3",
            "--cromossomo",
            "1",
            "--cruzamento",
            "1",
            "--saida",
            str(pasta),
        ]
    )
    assert df.iloc[0]["erros"] == 0
