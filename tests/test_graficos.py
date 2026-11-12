# ==============================
# tests/test_graficos.py
# ==============================
"""
# Testes de #37: um gráfico nunca pode interromper o benchmark nem custar os resultados.
"""

import pandas as pd
import pytest
import seaborn as sns

import main
from agents.genetic_agent import GeneticAgent
from utils import graficos
from world.world import World

GRAFICOS = {
    "memoria_cpu",
    "evolucao_fitness",
    "convergencia_populacao",
    "curva_convergencia_desvio_padrao",
    "violino_fitness",
    "ecdf_fitness_final",
    "mapa_de_calor_diversidade",
    "area_empilhada_diversidade",
    "pca_populacao_final",
}


def dados_do_ag(**parametros):
    return GeneticAgent(World(size=4, seed=1), **parametros).run()["dados_extra"]


def test_caso_normal_gera_os_nove_graficos(tmp_path):
    relatorio = graficos.gerar_graficos_avancados(
        dados_do_ag(population_size=20, gens=5, chrom_length=20), str(tmp_path)
    )
    assert set(relatorio["gerados"]) == GRAFICOS
    assert relatorio["pulados"] == [] and relatorio["falhas"] == []
    assert {p.stem for p in tmp_path.glob("*.png")} == GRAFICOS


@pytest.mark.parametrize(
    "parametros, pulados",
    [
        ({"population_size": 1, "gens": 5, "chrom_length": 10}, {"pca_populacao_final"}),
        ({"population_size": 10, "gens": 5, "chrom_length": 1, "crossover_rate": 0.0}, {"pca_populacao_final"}),
        (
            {"population_size": 10, "gens": 0, "chrom_length": 10},
            {
                "memoria_cpu",
                "evolucao_fitness",
                "convergencia_populacao",
                "curva_convergencia_desvio_padrao",
                "violino_fitness",
                "ecdf_fitness_final",
                "mapa_de_calor_diversidade",
                "area_empilhada_diversidade",
            },
        ),
    ],
    ids=["um_individuo", "um_gene", "zero_geracoes"],
)
def test_dados_insuficientes_pulam_o_grafico(parametros, pulados, tmp_path):
    relatorio = graficos.gerar_graficos_avancados(dados_do_ag(**parametros), str(tmp_path))
    assert set(relatorio["pulados"]) == pulados
    assert relatorio["falhas"] == []
    assert set(relatorio["gerados"]) == GRAFICOS - pulados


def test_falha_de_um_grafico_nao_impede_os_outros(tmp_path, monkeypatch, capsys):
    def explode(*args, **kwargs):
        raise RuntimeError("falha de propósito")

    monkeypatch.setattr(sns, "ecdfplot", explode)
    relatorio = graficos.gerar_graficos_avancados(
        dados_do_ag(population_size=20, gens=5, chrom_length=20), str(tmp_path)
    )
    assert relatorio["falhas"] == ["ecdf_fitness_final"]
    assert set(relatorio["gerados"]) == GRAFICOS - {"ecdf_fitness_final"}
    assert "falha de propósito" in capsys.readouterr().err


def test_falha_nos_graficos_basicos_nao_interrompe(tmp_path, monkeypatch, capsys):
    df = pd.DataFrame(
        [{"agente": "logico", "tamanho_mundo": 4, "vitorias": 1, "mortes": 0, "sobreviveu": 0, "tempo_medio": 0.1}]
    )
    original = graficos.plt.savefig

    def falha_so_em_mortes(caminho, *args, **kwargs):
        if "mortes" in str(caminho):
            raise OSError("falha de propósito")
        return original(caminho, *args, **kwargs)

    monkeypatch.setattr(graficos.plt, "savefig", falha_so_em_mortes)
    relatorio = graficos.gerar_graficos(df, str(tmp_path))
    assert relatorio["falhas"] == ["grafico_mortes"]
    assert len(relatorio["gerados"]) == 3
    assert "falha de propósito" in capsys.readouterr().err


@pytest.mark.parametrize(
    "extras",
    [
        ["--populacao", "1", "--geracoes", "5", "--cromossomo", "10"],
        ["--populacao", "10", "--geracoes", "5", "--cromossomo", "1", "--cruzamento", "0"],
        ["--populacao", "10", "--geracoes", "0", "--cromossomo", "10"],
    ],
    ids=["um_individuo", "um_gene", "zero_geracoes"],
)
def test_benchmark_termina_e_grava_os_resultados(extras, tmp_path):
    """Os três casos da issue #37: antes, o programa parava sem gravar o CSV."""
    pasta = tmp_path / "run"
    _, df = main.rodar_benchmark(
        ["--agentes", "genetico", "--tamanhos", "4", "--execucoes", "2", *extras, "--saida", str(pasta)]
    )
    assert (pasta / "resultados_benchmark.csv").exists()
    assert (pasta / "saida_terminal.txt").exists()
    assert len(df) == 1 and df.iloc[0]["erros"] == 0
