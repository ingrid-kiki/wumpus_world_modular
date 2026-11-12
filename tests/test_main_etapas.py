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
from agents.genetic_agent import AgenteGenetico
from world.world import Mundo

ARGS_AG = ["--populacao", "10", "--geracoes", "3", "--cromossomo", "10"]
GRAFICOS_AVANCADOS = {
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
GRAFICOS_BASICOS = {"grafico_vitorias", "grafico_mortes", "grafico_sobreviveu", "grafico_tempo_medio"}


def resultado_falso(agente, tamanho, dados_extra=None):
    return {
        "agente": agente,
        "tamanho_mundo": tamanho,
        "vitorias": 1,
        "mortes": 0,
        "sobreviveu": 0,
        "erros": 0,
        "tempo_total": 0.1,
        "tempo_medio": 0.1,
        "dados_extra": dados_extra or {},
    }


def benchmark_falso(monkeypatch, funcao):
    monkeypatch.setattr(main, "carregar_benchmark", lambda caminho: funcao)


def test_pastas_e_arquivos_completos_de_um_run(tmp_path):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        ["--agentes", "logico", "genetico", "--tamanhos", "4", "--execucoes", "2", *ARGS_AG, "--saida", str(pasta)]
    )
    assert {p.stem for p in (pasta / "graficos_avancados_genetico_4x4").glob("*.png")} == GRAFICOS_AVANCADOS
    assert not (pasta / "graficos_avancados_logico_4x4").exists()  # o agente lógico não tem dados extras
    assert {p.stem for p in pasta.glob("*.png")} >= GRAFICOS_BASICOS
    for arquivo in ("resultados_benchmark.csv", "saida_terminal.txt", "metadados.json", "dados_extra_genetico_4x4.npz"):
        assert (pasta / arquivo).exists(), arquivo
    assert not list(pasta.glob("*.log"))  # o registro único é o saida_terminal.txt
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
        main.rodar_benchmark(["--agentes", "logico", "--tamanhos", "4", "6", "--saida", str(pasta)])

    df = pd.read_csv(pasta / "resultados_benchmark.csv")
    assert list(df["tamanho_mundo"]) == [4]
    log = (pasta / "saida_terminal.txt").read_text(encoding="utf-8")
    assert "etapa 1 concluída" in log
    assert "RuntimeError: queda de propósito" in log


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
        main.rodar_benchmark(["--agentes", "logico", "--tamanhos", "4", "6", "--saida", str(pasta)])
    assert len(pd.read_csv(pasta / "resultados_benchmark.csv")) == 1
    assert "KeyboardInterrupt" in (pasta / "saida_terminal.txt").read_text(encoding="utf-8")


def test_log_e_gravado_durante_a_execucao(tmp_path):
    caminho = tmp_path / "saida.txt"
    with main.capturar_saida_terminal(str(caminho)):
        print("primeira linha")
        assert "primeira linha" in caminho.read_text(encoding="utf-8")


def test_graficos_avancados_valem_para_qualquer_agente_com_dados_extras(tmp_path, monkeypatch):
    dados = AgenteGenetico(
        Mundo(tamanho=4, semente=1), tamanho_populacao=10, geracoes=3, tamanho_cromossomo=10
    ).executar()["dados_extra"]
    benchmark_falso(
        monkeypatch, lambda agente, tamanho, execucoes, parametros_agentes=None: resultado_falso(agente, tamanho, dados)
    )
    pasta = tmp_path / "run"
    main.rodar_benchmark(["--agentes", "logico", "--tamanhos", "4", "--execucoes", "1", "--saida", str(pasta)])
    assert {p.stem for p in (pasta / "graficos_avancados_logico_4x4").glob("*.png")} == GRAFICOS_AVANCADOS
    assert (pasta / "dados_extra_logico_4x4.npz").exists()


def test_mensagem_conta_os_graficos_realmente_gerados(tmp_path, capsys):
    pasta = tmp_path / "run"
    main.rodar_benchmark(
        [
            "--agentes",
            "genetico",
            "--tamanhos",
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
    main.rodar_benchmark(["--agentes", "logico", "--tamanhos", "4", "--execucoes", "1", "--saida", str(pasta)])
    assert "Resultado nulo" in capsys.readouterr().out
