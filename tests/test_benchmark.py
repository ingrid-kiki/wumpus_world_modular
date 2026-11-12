# ==============================
# tests/test_benchmark.py
# ==============================
"""
# Testes do benchmark único (benchmark.py): os modos sequencial e paralelo dão os mesmos resultados,
# o modo silencioso esconde as mensagens, os tempos têm o significado documentado e as opções
# --paralelo e --silencioso chegam do main.py.
"""

import benchmark
import main

AG_RAPIDO = {"genetico": {"population_size": 10, "gens": 4, "chrom_length": 12}}
CONTAGENS = ("vitorias", "mortes", "sobreviveu", "erros")


def test_modos_sequencial_e_paralelo_dao_os_mesmos_resultados():
    for agente, tamanho in (("logico_seguro", 6), ("genetico", 4)):
        sequencial = benchmark.executar_benchmark(agente, tamanho, 6, AG_RAPIDO, silencioso=True)
        paralelo = benchmark.executar_benchmark(agente, tamanho, 6, AG_RAPIDO, paralelo=True, silencioso=True)
        assert {c: sequencial[c] for c in CONTAGENS} == {c: paralelo[c] for c in CONTAGENS}, agente
        assert bool(sequencial["dados_extra"]) == bool(paralelo["dados_extra"])


def test_silencioso_esconde_as_mensagens(capsys):
    benchmark.executar_benchmark("logico", 4, 2)
    normal = capsys.readouterr().out
    benchmark.executar_benchmark("logico", 4, 2, silencioso=True)
    silencioso = capsys.readouterr().out
    assert "Execução 1/2" in normal and "[Passo 1]" in normal
    assert silencioso == ""


def test_tempo_total_e_de_relogio_e_tempo_medio_e_a_media_das_execucoes():
    execucoes = [
        {"status": "vitoria", "tempo": 2.0, "dados_extra": {}},
        {"status": "morte", "tempo": 4.0, "dados_extra": {"fitness": [1.0]}},
    ]
    resumo = benchmark.resumir("x", 4, execucoes, tempo_de_relogio=3.5)
    assert resumo["tempo_total"] == 3.5  # num run paralelo, menor que a soma dos tempos (6 s)
    assert resumo["tempo_medio"] == 3.0
    assert resumo["dados_extra"] == {"fitness": [1.0]}
    assert (resumo["vitorias"], resumo["mortes"]) == (1, 1)


def test_opcoes_do_main_chegam_ao_benchmark(tmp_path, monkeypatch):
    recebidos = []

    def benchmark_falso(agente, tamanho, execucoes, parametros_agentes=None, **modos):
        recebidos.append(modos)
        return benchmark.resumir(agente, tamanho, [{"status": "sobreviveu", "tempo": 0.0, "dados_extra": {}}], 0.0)

    monkeypatch.setattr(main, "carregar_benchmark", lambda caminho: benchmark_falso)
    comum = ["--agentes", "logico", "--tamanhos", "4", "--execucoes", "1"]
    main.rodar_benchmark([*comum, "--paralelo", "--silencioso", "--saida", str(tmp_path / "com")])
    main.rodar_benchmark([*comum, "--saida", str(tmp_path / "sem")])
    # Sem as opções, nada é repassado: um benchmark externo sem esses parâmetros continua funcionando
    assert recebidos == [{"paralelo": True, "silencioso": True}, {}]
