# ==============================
# utils/graficos.py
# ==============================
"""
# Este módulo centraliza todas as funções de geração de gráficos do projeto Wumpus World.
# Ele inclui funções para criar gráficos básicos (barras, tempo médio) e avançados
# (memória/CPU, evolução do fitness, convergência, violino, ECDF, mapas de calor,
# área empilhada e PCA) a partir dos dados coletados nos benchmarks dos agentes.
# Todos os gráficos são salvos automaticamente nas pastas de saída organizadas por execução.
#
# Um gráfico nunca interrompe o benchmark (#37): se não houver dados suficientes, ele é pulado;
# se falhar, o erro vai para o stderr e os demais gráficos continuam.
"""

import matplotlib

matplotlib.use("Agg")  # só salva arquivos, nunca abre janela (evita depender do Tk)
import os
import sys
import traceback

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA

# Coluna do CSV (sem acento) e o nome que aparece no título do gráfico (com acento)
METRICAS_BASICAS = {"vitorias": "Vitórias", "mortes": "Mortes", "sobreviveu": "Sobreviveu"}


def _desenhar(nome, funcao, relatorio):
    """Roda a função de um gráfico; uma falha fica no relatório e no stderr, sem interromper os demais."""
    try:
        funcao()
        relatorio["gerados"].append(nome)
    except Exception as e:  # um gráfico não pode custar os resultados do benchmark
        relatorio["falhas"].append(nome)
        print(f"⚠️ Gráfico '{nome}' não foi gerado: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    finally:
        plt.close("all")  # não deixa figura aberta para o próximo gráfico


def _relatorio_vazio():
    return {"gerados": [], "pulados": [], "falhas": []}


def _salvar(output_dir, nome):
    """Ajusta o layout, salva a figura atual como <nome>.png e a fecha."""
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{nome}.png"))
    plt.close()


# ---------------------------------------------------------------- Gráficos básicos


def _barras_por_tamanho(df, coluna, titulo, rotulo_y, nome, output_dir):
    """Barras de uma coluna do resumo, com um grupo por tamanho de mundo e uma barra por agente."""
    plt.figure(figsize=(8, 5))
    for tamanho in sorted(df["tamanho_mundo"].unique()):
        subset = df[df["tamanho_mundo"] == tamanho]
        plt.bar(
            [f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
            subset[coluna],
            label=f"{tamanho}x{tamanho}",
        )
    plt.title(titulo)
    plt.ylabel(rotulo_y)
    plt.xlabel("Agente-Tamanho")
    plt.xticks(rotation=45)
    _salvar(output_dir, nome)


def gerar_graficos(df, output_dir):
    """
    Gera gráficos básicos de barras para vitórias, mortes, sobrevivências e tempo médio.
    Salva cada gráfico na pasta de saída especificada.
    :return: dict com os nomes em "gerados", "pulados" e "falhas"
    """
    relatorio = _relatorio_vazio()
    for metric, rotulo in METRICAS_BASICAS.items():
        titulo = f"Comparação de {rotulo} por agente e tamanho do mundo"
        _desenhar(
            f"grafico_{metric}",
            lambda m=metric, t=titulo: _barras_por_tamanho(df, m, t, "Quantidade", f"grafico_{m}", output_dir),
            relatorio,
        )
    _desenhar(
        "grafico_tempo_medio",
        lambda: _barras_por_tamanho(
            df,
            "tempo_medio",
            "Tempo médio de execução por agente e tamanho do mundo",
            "Tempo médio (s)",
            "grafico_tempo_medio",
            output_dir,
        ),
        relatorio,
    )
    return relatorio


# ---------------------------------------------------------------- Gráficos avançados


def _matriz(dados_extra, chave):
    """Devolve dados_extra[chave] como matriz 2D não vazia, ou None se não houver dados para isso."""
    if chave not in dados_extra or dados_extra[chave] is None:
        return None
    matriz = np.asarray(dados_extra[chave])
    return matriz if matriz.ndim == 2 and matriz.size > 0 else None


def _serie(dados_extra, chave):
    """Devolve dados_extra[chave] se for uma sequência não vazia, ou None."""
    valor = dados_extra.get(chave)
    return valor if valor is not None and len(valor) > 0 else None


def _dados_avancados(dados_extra):
    """Séries e matrizes usadas pelos gráficos avançados; None onde não há dados suficientes."""
    return {
        "memoria": _serie(dados_extra, "memoria"),
        "cpu": _serie(dados_extra, "cpu"),
        "fitness": _serie(dados_extra, "fitness"),
        "fitness_pop": _matriz(dados_extra, "fitness_pop"),  # (gerações, população)
        "fitness_final": _serie(dados_extra, "fitness_final"),
        "diversidade": _matriz(dados_extra, "diversidade_vars"),  # (gerações, variáveis)
        "pop_final": _matriz(dados_extra, "pop_final"),  # (indivíduos, genes)
    }


def _memoria_cpu(d, output_dir):
    """Uso de memória e de CPU ao longo das gerações."""
    plt.figure(figsize=(10, 5))
    plt.plot(d["memoria"], label="Memória (MB)")
    plt.plot(d["cpu"], label="CPU (%)")
    plt.title("Uso de Memória e CPU durante Execução")
    plt.xlabel("Iteração")
    plt.ylabel("Uso")
    plt.legend()
    _salvar(output_dir, "memoria_cpu")


def _evolucao_fitness(d, output_dir):
    """Fitness médio por geração (convergência)."""
    plt.figure(figsize=(8, 5))
    plt.plot(d["fitness"])
    plt.title("Evolução do Fitness (Convergência)")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    _salvar(output_dir, "evolucao_fitness")


def _convergencia_populacao(d, output_dir):
    """Fitness mínimo, médio e máximo da população em cada geração."""
    fitness_pop = d["fitness_pop"]
    plt.figure(figsize=(8, 5))
    plt.plot(np.min(fitness_pop, axis=1), label="Mínimo")
    plt.plot(np.mean(fitness_pop, axis=1), label="Médio")
    plt.plot(np.max(fitness_pop, axis=1), label="Máximo")
    plt.title("Comportamento de Convergência da População")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.legend()
    _salvar(output_dir, "convergencia_populacao")


def _curva_convergencia_desvio_padrao(d, output_dir):
    """Média do fitness por geração, com uma faixa de um desvio padrão."""
    mean = np.mean(d["fitness_pop"], axis=1)
    std = np.std(d["fitness_pop"], axis=1)
    plt.figure(figsize=(8, 5))
    plt.plot(mean, label="Média")
    plt.fill_between(range(len(mean)), mean - std, mean + std, alpha=0.3, label="Desvio Padrão")
    plt.title("Média das Curvas de Convergência com Desvio Padrão")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.legend()
    _salvar(output_dir, "curva_convergencia_desvio_padrao")


def _violino_fitness(d, output_dir):
    """Distribuição do fitness da população em cada geração."""
    plt.figure(figsize=(8, 5))
    sns.violinplot(data=d["fitness_pop"].T)
    plt.title("Distribuição do Fitness por Geração (Violin Plot)")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    _salvar(output_dir, "violino_fitness")


def _ecdf_fitness_final(d, output_dir):
    """Função de distribuição acumulada do fitness da última geração."""
    plt.figure(figsize=(8, 5))
    sns.ecdfplot(d["fitness_final"])
    plt.title("Função de Distribuição Acumulada do Fitness Final")
    plt.xlabel("Fitness")
    _salvar(output_dir, "ecdf_fitness_final")


def _mapa_de_calor_diversidade(d, output_dir):
    """Quantos genes diferentes há em cada posição do cromossomo, geração a geração."""
    plt.figure(figsize=(10, 6))
    sns.heatmap(d["diversidade"], cmap="viridis")
    plt.title("Mapa de Calor da Diversidade por Variável")
    plt.xlabel("Variável")
    plt.ylabel("Geração")
    _salvar(output_dir, "mapa_de_calor_diversidade")


def _area_empilhada_diversidade(d, output_dir):
    """A mesma diversidade do mapa de calor, empilhada por geração."""
    diversidade = d["diversidade"]
    plt.figure(figsize=(10, 6))
    # Cada linha de diversidade_vars é uma geração, cada coluna uma variável
    plt.stackplot(range(diversidade.shape[0]), diversidade.T)
    plt.title("Área Empilhada da Diversidade por Variável")
    plt.xlabel("Geração")
    plt.ylabel("Diversidade")
    _salvar(output_dir, "area_empilhada_diversidade")


def _pca_populacao_final(d, output_dir):
    """Projeção em duas dimensões (PCA) dos cromossomos da população final."""
    x_pca = PCA(n_components=2).fit_transform(d["pop_final"])
    plt.figure(figsize=(8, 6))
    plt.scatter(x_pca[:, 0], x_pca[:, 1], alpha=0.7)
    plt.title("PCA dos Indivíduos da População Final")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    _salvar(output_dir, "pca_populacao_final")


# Cada gráfico com a condição para existir: com dados insuficientes, ele é pulado
GRAFICOS_AVANCADOS = [
    ("memoria_cpu", _memoria_cpu, lambda d: d["memoria"] is not None and d["cpu"] is not None),
    ("evolucao_fitness", _evolucao_fitness, lambda d: d["fitness"] is not None),
    ("convergencia_populacao", _convergencia_populacao, lambda d: d["fitness_pop"] is not None),
    ("curva_convergencia_desvio_padrao", _curva_convergencia_desvio_padrao, lambda d: d["fitness_pop"] is not None),
    ("violino_fitness", _violino_fitness, lambda d: d["fitness_pop"] is not None),
    ("ecdf_fitness_final", _ecdf_fitness_final, lambda d: d["fitness_final"] is not None),
    ("mapa_de_calor_diversidade", _mapa_de_calor_diversidade, lambda d: d["diversidade"] is not None),
    ("area_empilhada_diversidade", _area_empilhada_diversidade, lambda d: d["diversidade"] is not None),
    # O PCA de 2 componentes precisa de pelo menos 2 indivíduos e 2 genes
    (
        "pca_populacao_final",
        _pca_populacao_final,
        lambda d: d["pop_final"] is not None and min(d["pop_final"].shape) >= 2,
    ),
]


def gerar_graficos_avancados(dados_extra, output_dir):
    """
    Gera gráficos avançados a partir dos dados extras coletados durante as execuções.
    Cada gráfico é salvo na pasta de saída. Os dados esperados devem estar em arrays/listas.
    Gráficos sem dados suficientes são pulados e falhas não interrompem os demais (#37).
    :return: dict com os nomes em "gerados", "pulados" e "falhas"
    """
    relatorio = _relatorio_vazio()
    dados = _dados_avancados(dados_extra)
    for nome, funcao, tem_dados in GRAFICOS_AVANCADOS:
        if tem_dados(dados):
            _desenhar(nome, lambda f=funcao: f(dados, output_dir), relatorio)
        else:
            relatorio["pulados"].append(nome)

    if relatorio["pulados"]:
        print(f"ℹ️ Gráficos pulados por falta de dados: {', '.join(relatorio['pulados'])}")
    return relatorio
