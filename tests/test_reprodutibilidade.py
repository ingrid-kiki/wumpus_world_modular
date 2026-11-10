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
from agents.genetic_agent import GeneticAgent
from ga.ga_core import GeneticAlgorithm
from ga.individual import Individual
from utils.versao import __version__
from world.world import World

# Benchmark pequeno e completo (os dois agentes), usado por vários testes
ARGS_PEQUENOS = [
    "--agentes",
    "logico",
    "genetico",
    "--sizes",
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
    assert main.parametros_do_ag(args) == {"population_size": 30, "crossover_rate": 0.5}


def test_sem_opcoes_do_ag_valem_os_padroes():
    args = main.criar_parser().parse_args([])
    assert main.parametros_do_ag(args) == {}


def test_benchmark_repassa_os_parametros_so_para_o_agente_certo(monkeypatch):
    recebidos = {}

    class Gravador:
        def __init__(self, world, **kwargs):
            self.world, self.logger = world, None
            recebidos.setdefault("kwargs", []).append(kwargs)

        def run(self):
            return {}

    monkeypatch.setitem(benchmark.AGENTES_DISPONIVEIS, "gravador", Gravador)
    benchmark.executar_benchmark("gravador", 4, 2, parametros_agentes={"gravador": {"gens": 7}, "outro": {"x": 1}})
    assert recebidos["kwargs"] == [{"gens": 7}, {"gens": 7}]


# ---------------------------------------------------------------- metadata.json


def test_run_grava_metadata_completo(run_pequeno):
    meta = json.loads((run_pequeno / "metadata.json").read_text(encoding="utf-8"))
    assert meta["versao"] == __version__
    assert set(meta["git"]) == {"commit", "branch", "alteracoes_nao_commitadas", "arquivos_alterados"}
    assert meta["argumentos_cli"][: len(ARGS_PEQUENOS)] == ARGS_PEQUENOS
    assert meta["parametros_ag"]["population_size"] == 20
    assert meta["parametros_ag"]["gens"] == 15
    assert meta["parametros_ag"]["mutation_rate"] == 0.1
    assert meta["parametros_ag"]["crossover_rate"] == 0.8  # padrão do GeneticAgent
    assert "seed=i" in meta["sementes"]
    assert meta["bibliotecas"]["numpy"]


def test_sem_agente_genetico_nao_ha_parametros_do_ag(tmp_path):
    main.rodar_benchmark(["--agentes", "logico", "--sizes", "4", "--execucoes", "1", "--saida", str(tmp_path)])
    meta = json.loads((tmp_path / "metadata.json").read_text(encoding="utf-8"))
    assert meta["parametros_ag"] is None


# ---------------------------------------------------------------- reproduzir.py


def test_reproduzir_da_o_mesmo_resultado(run_pequeno, tmp_path):
    assert reproduzir.main([str(run_pequeno), "--saida", str(tmp_path / "copia")]) == 0


def test_reproduzir_detecta_resultado_diferente(run_pequeno, tmp_path):
    copia = tmp_path / "adulterado"
    copia.mkdir()
    (copia / "metadata.json").write_text((run_pequeno / "metadata.json").read_text(encoding="utf-8"), encoding="utf-8")
    csv = (run_pequeno / "resultados_benchmark.csv").read_text(encoding="utf-8").splitlines()
    cab, linha = csv[0], csv[1].split(",")
    linha[2] = str(int(linha[2]) + 1)  # uma vitória a mais
    (copia / "resultados_benchmark.csv").write_text("\n".join([cab, ",".join(linha), *csv[2:]]), encoding="utf-8")
    assert reproduzir.main([str(copia), "--saida", str(tmp_path / "nova")]) == 1


def test_reproduzir_sem_metadata(tmp_path):
    assert reproduzir.main([str(tmp_path)]) == 2


def test_sem_opcao_remove_opcao_e_valor():
    assert reproduzir.sem_opcao(["--a", "1", "--saida", "x", "--b"], "--saida") == ["--a", "1", "--b"]
    assert reproduzir.sem_opcao(["--saida=x", "--b"], "--saida") == ["--b"]


# ---------------------------------------------------------------- Otimizações do AG


def test_clone_do_mundo_e_independente():
    w = World(size=4, seed=1)
    c = w.clone()
    c.step("BAIXO")
    c.pits.append((9, 9))
    c.wumpus_alive = False
    assert c.agent_pos == (1, 0)
    assert w.agent_pos == (0, 0)
    assert len(w.pits) == 2 and (9, 9) not in w.pits
    assert w.wumpus_alive and w.is_alive and not w.won


def test_copia_do_individuo_e_independente():
    ind = Individual(5)
    ind.fitness = 3.0
    copia = ind.copia()
    copia.chromosome[0] = "OUTRA"
    assert ind.chromosome[0] != "OUTRA" and copia.fitness == 3.0


def test_cache_nao_muda_o_resultado_do_ag():
    w = World(size=4, seed=2)
    com_cache = GeneticAlgorithm(pop_size=20, gens=15, chrom_length=20, mutation_rate=0.05, crossover_rate=0.5, seed=2)
    r1 = com_cache.run(w)

    sem_cache = GeneticAlgorithm(pop_size=20, gens=15, chrom_length=20, mutation_rate=0.05, crossover_rate=0.5, seed=2)
    sem_cache.avaliar = lambda ind, world: ind.evaluate(world)  # desliga o cache
    r2 = sem_cache.run(w)

    assert r1["best"].chromosome == r2["best"].chromosome
    assert r1["fitness_pop"] == r2["fitness_pop"]
    assert r1["acertos_cache"] > 0


def test_agente_genetico_com_parametros_da_cli_e_reprodutivel():
    acoes = []
    for _ in range(2):
        r = GeneticAgent(World(size=4, seed=5), population_size=20, gens=10, chrom_length=20).run()
        acoes.append([p["ação"] for p in r["history"]])
    assert acoes[0] == acoes[1]
