# ==============================
# tests/test_reprodutibilidade.py
# ==============================
"""
# Testes da Fase 4 (#17): metadados por execução, parâmetros do AG pela linha de comando (#13),
# reprodução de um run e as otimizações do AG, que não podem mudar resultados.
"""

import json

import pytest

import benchmark
import main
import reproduzir
from agents.genetic_agent import AgenteGenetico
from ga.ga_core import AlgoritmoGenetico
from ga.individual import Individuo
from utils.versao import __version__
from world.world import Mundo

# Benchmark pequeno e completo (os dois agentes), usado por vários testes
ARGS_PEQUENOS = [
    "--agentes",
    "logico",
    "genetico",
    "--tamanhos",
    "4",
    "--execucoes",
    "3",
    "--populacao",
    "20",
    "--geracoes",
    "15",
    "--cromossomo",
    "20",
    "--mutacao",
    "0.1",
]


@pytest.fixture(scope="module")
def run_pequeno(tmp_path_factory):
    pasta = tmp_path_factory.mktemp("run") / "original"
    main.rodar_benchmark(ARGS_PEQUENOS + ["--saida", str(pasta)])
    return pasta


# ---------------------------------------------------------------- Linha de comando


def test_parametros_do_ag_vem_da_linha_de_comando():
    args = main.criar_parser().parse_args(["--populacao", "30", "--cruzamento", "0.5"])
    assert main.parametros_do_ag(args) == {"tamanho_populacao": 30, "taxa_cruzamento": 0.5}


def test_sem_opcoes_do_ag_valem_os_padroes():
    args = main.criar_parser().parse_args([])
    assert main.parametros_do_ag(args) == {}


def test_benchmark_repassa_os_parametros_so_para_o_agente_certo(monkeypatch):
    recebidos = {}

    class Gravador:
        def __init__(self, mundo, **kwargs):
            self.mundo = mundo
            recebidos.setdefault("kwargs", []).append(kwargs)

        def executar(self):
            return {}

    monkeypatch.setitem(benchmark.AGENTES_DISPONIVEIS, "gravador", Gravador)
    benchmark.executar_benchmark("gravador", 4, 2, parametros_agentes={"gravador": {"geracoes": 7}, "outro": {"x": 1}})
    assert recebidos["kwargs"] == [{"geracoes": 7}, {"geracoes": 7}]


# ---------------------------------------------------------------- metadados.json


def test_run_grava_metadados_completos(run_pequeno):
    meta = json.loads((run_pequeno / "metadados.json").read_text(encoding="utf-8"))
    assert meta["versao"] == __version__
    assert set(meta["git"]) == {"commit", "branch", "alteracoes_nao_commitadas", "arquivos_alterados"}
    assert meta["argumentos_cli"][: len(ARGS_PEQUENOS)] == ARGS_PEQUENOS
    assert meta["parametros_ag"]["tamanho_populacao"] == 20
    assert meta["parametros_ag"]["geracoes"] == 15
    assert meta["parametros_ag"]["taxa_mutacao"] == 0.1
    assert meta["parametros_ag"]["taxa_cruzamento"] == 0.8  # padrão do AgenteGenetico
    assert "semente=i" in meta["sementes"]
    assert meta["bibliotecas"]["numpy"]


def test_sem_agente_genetico_nao_ha_parametros_do_ag(tmp_path):
    main.rodar_benchmark(["--agentes", "logico", "--tamanhos", "4", "--execucoes", "1", "--saida", str(tmp_path)])
    meta = json.loads((tmp_path / "metadados.json").read_text(encoding="utf-8"))
    assert meta["parametros_ag"] is None


# ---------------------------------------------------------------- reproduzir.py


def test_reproduzir_da_o_mesmo_resultado(run_pequeno, tmp_path):
    assert reproduzir.main([str(run_pequeno), "--saida", str(tmp_path / "copia")]) == 0


def test_reproduzir_detecta_resultado_diferente(run_pequeno, tmp_path):
    copia = tmp_path / "adulterado"
    copia.mkdir()
    (copia / "metadados.json").write_text(
        (run_pequeno / "metadados.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    csv = (run_pequeno / "resultados_benchmark.csv").read_text(encoding="utf-8").splitlines()
    cab, linha = csv[0], csv[1].split(",")
    linha[2] = str(int(linha[2]) + 1)  # uma vitória a mais
    (copia / "resultados_benchmark.csv").write_text("\n".join([cab, ",".join(linha), *csv[2:]]), encoding="utf-8")
    assert reproduzir.main([str(copia), "--saida", str(tmp_path / "nova")]) == 1


def test_reproduzir_le_um_run_antigo(run_pequeno, tmp_path):
    """Runs gravados até a v1.8.0: metadata.json, opção --sizes e colunas com acento."""
    antigo = tmp_path / "antigo"
    antigo.mkdir()
    meta = json.loads((run_pequeno / "metadados.json").read_text(encoding="utf-8"))
    meta["argumentos_cli"] = ["--sizes" if a == "--tamanhos" else a for a in meta["argumentos_cli"]]
    (antigo / "metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    csv = (run_pequeno / "resultados_benchmark.csv").read_text(encoding="utf-8")
    csv = csv.replace("vitorias", "vitórias").replace("tempo_medio", "tempo_médio")
    (antigo / "resultados_benchmark.csv").write_text(csv, encoding="utf-8")
    assert reproduzir.main([str(antigo), "--saida", str(tmp_path / "nova")]) == 0


def test_atualizar_opcoes_troca_as_opcoes_antigas():
    assert reproduzir.atualizar_opcoes(["--sizes", "4", "--execucoes=2"]) == ["--tamanhos", "4", "--execucoes=2"]
    assert reproduzir.atualizar_opcoes(["--sizes=4"]) == ["--tamanhos=4"]


def test_atualizar_opcoes_troca_benchmarks_retirados():
    """Os 4 benchmarks retirados na #76 davam os mesmos resultados: o benchmark.py os substitui."""
    assert reproduzir.atualizar_opcoes(["--benchmark", "benchmark_fast.py"]) == ["--benchmark", "benchmark.py"]
    assert reproduzir.atualizar_opcoes(["--benchmark=pasta/benchmark_sideB.py"]) == ["--benchmark=benchmark.py"]
    assert reproduzir.atualizar_opcoes(["--benchmark", "meu.py"]) == ["--benchmark", "meu.py"]


def test_reproduzir_sem_metadados(tmp_path):
    assert reproduzir.main([str(tmp_path)]) == 2


def test_sem_opcao_remove_opcao_e_valor():
    assert reproduzir.sem_opcao(["--a", "1", "--saida", "x", "--b"], "--saida") == ["--a", "1", "--b"]
    assert reproduzir.sem_opcao(["--saida=x", "--b"], "--saida") == ["--b"]


# ---------------------------------------------------------------- Otimizações do AG


def test_clone_do_mundo_e_independente():
    w = Mundo(tamanho=4, semente=1)
    c = w.clonar()
    c.agir("BAIXO")
    c.pocos.append((9, 9))
    c.wumpus_vivo = False
    assert c.posicao_agente == (1, 0)
    assert w.posicao_agente == (0, 0)
    assert len(w.pocos) == 2 and (9, 9) not in w.pocos
    assert w.wumpus_vivo and w.agente_vivo and not w.ganhou


def test_copia_do_individuo_e_independente():
    ind = Individuo(5)
    ind.fitness = 3.0
    copia = ind.copia()
    copia.cromossomo[0] = "OUTRA"
    assert ind.cromossomo[0] != "OUTRA" and copia.fitness == 3.0


def test_cache_nao_muda_o_resultado_do_ag():
    w = Mundo(tamanho=4, semente=2)
    com_cache = AlgoritmoGenetico(
        tamanho_populacao=20, geracoes=15, tamanho_cromossomo=20, taxa_mutacao=0.05, taxa_cruzamento=0.5, semente=2
    )
    r1 = com_cache.executar(w)

    sem_cache = AlgoritmoGenetico(
        tamanho_populacao=20, geracoes=15, tamanho_cromossomo=20, taxa_mutacao=0.05, taxa_cruzamento=0.5, semente=2
    )
    sem_cache.avaliar = lambda ind, mundo: ind.avaliar(mundo)  # desliga o cache
    r2 = sem_cache.executar(w)

    assert r1["melhor"].cromossomo == r2["melhor"].cromossomo
    assert r1["fitness_pop"] == r2["fitness_pop"]
    assert r1["acertos_cache"] > 0


def test_agente_genetico_com_parametros_da_cli_e_reprodutivel():
    acoes = []
    for _ in range(2):
        r = AgenteGenetico(
            Mundo(tamanho=4, semente=5), tamanho_populacao=20, geracoes=10, tamanho_cromossomo=20
        ).executar()
        acoes.append([p["acao"] for p in r["historico"]])
    assert acoes[0] == acoes[1]
