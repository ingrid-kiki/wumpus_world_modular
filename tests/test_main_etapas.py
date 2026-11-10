# ==============================
# tests/test_main_etapas.py
# ==============================
"""
# Garante o que cada etapa do laço de main.rodar_benchmark() precisa entregar: pastas e arquivos
# por agente e tamanho, gráficos avançados de quem tem dados extras e resultados que sobrevivem
# a uma interrupção. Estes testes substituem o antigo comentário "NÃO ALTERAR" daquele trecho.
"""

import pandas as pd
import pytest

import main
from agents.genetic_agent import GeneticAgent
from world.world import World

ARGS_AG = ["--populacao", "10", "--geracoes", "3", "--cromossomo", "10"]
GRAFICOS_AVANCADOS = {
    "memoria_cpu",
    "evolucao_fitness",
    "convergencia_populacao",
    "curva_convergencia_std",
    "violin_fitness",
    "ecdf_fitness_final",
    "heatmap_diversidade",
    "area_empilhada_diversidade",
    "pca_populacao_final",
}
GRAFICOS_BASICOS = {"grafico_vitórias", "grafico_mortes", "grafico_sobreviveu", "grafico_tempo_medio"}


def resultado_falso(agente, tamanho, dados_extra=None):
    return {
        "agente": agente,
        "tamanho_mundo": tamanho,
        "vitórias": 1,
        "mortes": 0,
        "sobreviveu": 0,
        "erros": 0,
        "tempo_total": 0.1,
        "tempo_médio": 0.1,
        "dados_extra": dados_extra or {},
    }


def benchmark_falso(monkeypatch, funcao):
    monkeypatch.setattr(main, "carregar_benchmark", lambda caminho: funcao)


def test_layout_completo_de_um_run(tmp_path):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        ["--agentes", "logico", "genetico", "--sizes", "4", "--execucoes", "2", *ARGS_AG, "--saida", str(pasta)]
    )
    assert {p.stem for p in (pasta / "advanced_charts_genetico_4x4").glob("*.png")} == GRAFICOS_AVANCADOS
    assert not (pasta / "advanced_charts_logico_4x4").exists()  # o agente lógico não tem dados extras
    assert GRAFICOS_BASICOS <= {p.stem for p in pasta.glob("*.png")}
    for arquivo in ("resultados_benchmark.csv", "terminal_output.txt", "metadata.json", "dados_extra_genetico_4x4.npz"):
        assert (pasta / arquivo).exists(), arquivo
    assert len(list(pasta.glob("logico_*.log"))) == 1 and len(list(pasta.glob("genetico_*.log"))) == 1
    assert not list(pasta.rglob("*.tmp"))
    assert len(pd.read_csv(pasta / "resultados_benchmark.csv")) == 2


def test_queda_na_segunda_etapa_preserva_a_primeira(tmp_path, monkeypatch):
    chamadas = []

    def falha_na_segunda(agente, tamanho, execucoes, parametros_agentes=None):
        chamadas.append(agente)
        if len(chamadas) == 2:
            raise RuntimeError("queda de propósito")
        print("etapa 1 concluída")
        return resultado_falso(agente, tamanho)

    benchmark_falso(monkeypatch, falha_na_segunda)
    pasta = tmp_path / "run"
    with pytest.raises(RuntimeError, match="queda de propósito"):
        main.rodar_benchmark(["--agentes", "logico", "--sizes", "4", "6", "--saida", str(pasta)])

    df = pd.read_csv(pasta / "resultados_benchmark.csv")
    assert list(df["tamanho_mundo"]) == [4]
    log = (pasta / "terminal_output.txt").read_text(encoding="utf-8")
    assert "etapa 1 concluída" in log
    assert "RuntimeError: queda de propósito" in log
    for arquivo in pasta.glob("*.log"):
        arquivo.unlink()  # no Windows, falha se o logger da etapa interrompida não tiver sido fechado


def test_ctrl_c_tambem_preserva_resultados_e_log(tmp_path, monkeypatch):
    chamadas = []

    def interrompe(agente, tamanho, execucoes, parametros_agentes=None):
        chamadas.append(agente)
        if len(chamadas) == 2:
            raise KeyboardInterrupt
        return resultado_falso(agente, tamanho)

    benchmark_falso(monkeypatch, interrompe)
    pasta = tmp_path / "run"
    with pytest.raises(KeyboardInterrupt):
        main.rodar_benchmark(["--agentes", "logico", "--sizes", "4", "6", "--saida", str(pasta)])
    assert len(pd.read_csv(pasta / "resultados_benchmark.csv")) == 1
    assert "KeyboardInterrupt" in (pasta / "terminal_output.txt").read_text(encoding="utf-8")


def test_log_e_gravado_durante_a_execucao(tmp_path):
    caminho = tmp_path / "saida.txt"
    with main.capturar_saida_terminal(str(caminho)):
        print("primeira linha")
        assert "primeira linha" in caminho.read_text(encoding="utf-8")


def test_graficos_avancados_valem_para_qualquer_agente_com_dados_extras(tmp_path, monkeypatch):
    dados = GeneticAgent(World(size=4, seed=1), population_size=10, gens=3, chrom_length=10).run()["dados_extra"]
    benchmark_falso(
        monkeypatch, lambda agente, tamanho, execucoes, parametros_agentes=None: resultado_falso(agente, tamanho, dados)
    )
    pasta = tmp_path / "run"
    main.rodar_benchmark(["--agentes", "logico", "--sizes", "4", "--execucoes", "1", "--saida", str(pasta)])
    assert {p.stem for p in (pasta / "advanced_charts_logico_4x4").glob("*.png")} == GRAFICOS_AVANCADOS
    assert (pasta / "dados_extra_logico_4x4.npz").exists()


def test_mensagem_conta_os_graficos_realmente_gerados(tmp_path, capsys):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        [
            "--agentes",
            "genetico",
            "--sizes",
            "4",
            "--execucoes",
            "1",
            "--populacao",
            "1",
            "--geracoes",
            "3",
            "--cromossomo",
            "10",
            "--saida",
            str(pasta),
        ]
    )
    saida = capsys.readouterr().out
    assert "8 salvos em" in saida  # o PCA é pulado com um único indivíduo
    assert "pca_populacao_final" in saida


def test_benchmark_externo_que_devolve_none_nao_derruba(tmp_path, monkeypatch, capsys):
    benchmark_falso(monkeypatch, lambda agente, tamanho, execucoes, parametros_agentes=None: None)
    pasta = tmp_path / "run"
    main.rodar_benchmark(["--agentes", "logico", "--sizes", "4", "--execucoes", "1", "--saida", str(pasta)])
    assert "Resultado nulo" in capsys.readouterr().out
