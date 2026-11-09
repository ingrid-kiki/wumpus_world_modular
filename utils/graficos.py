# ==============================
# utils/graficos.py
# ==============================
'''
# Este módulo centraliza todas as funções de geração de gráficos do projeto Wumpus World.
# Ele inclui funções para criar gráficos básicos (barras, tempo médio) e avançados
# (memória/CPU, evolução do fitness, convergência, violino, ECDF, mapas de calor,
# área empilhada e PCA) a partir dos dados coletados nos benchmarks dos agentes.
# Todos os gráficos são salvos automaticamente nas pastas de saída organizadas por execução.
#
# Um gráfico nunca interrompe o benchmark (#37): se não houver dados suficientes, ele é pulado;
# se falhar, o erro vai para o stderr e os demais gráficos continuam.
'''

import matplotlib
matplotlib.use("Agg")  # só salva arquivos, nunca abre janela (evita depender do Tk)
import matplotlib.pyplot as plt  # noqa: E402
import os
import sys
import traceback
from sklearn.decomposition import PCA
import seaborn as sns
import numpy as np


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


def gerar_graficos(df, output_dir):
    """
    Gera gráficos básicos de barras para vitórias, mortes, sobrevivências e tempo médio.
    Salva cada gráfico na pasta de saída especificada.
    :return: dict com os nomes em "gerados", "pulados" e "falhas"
    """
    relatorio = _relatorio_vazio()

    # Gera gráficos de barras para vitórias, mortes e sobrevivências
    def barras(metric):
        plt.figure(figsize=(8, 5))
        # Para cada tamanho de mundo, plota as barras dos agentes
        for tamanho in sorted(df["tamanho_mundo"].unique()):
            subset = df[df["tamanho_mundo"] == tamanho]
            plt.bar([f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
                    subset[metric], label=f"{tamanho}x{tamanho}")
        plt.title(f"Comparação de {metric.capitalize()} por agente e tamanho do mundo")
        plt.ylabel("Quantidade")
        plt.xlabel("Agente-Tamanho")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"grafico_{metric}.png"))
        plt.close()

    # Gráfico de barras para o tempo médio de execução por agente e tamanho
    def tempo_medio():
        plt.figure(figsize=(8, 5))
        for tamanho in sorted(df["tamanho_mundo"].unique()):
            subset = df[df["tamanho_mundo"] == tamanho]
            plt.bar([f"{row['agente']}-{tamanho}" for _, row in subset.iterrows()],
                    subset["tempo_médio"], label=f"{tamanho}x{tamanho}")
        plt.title("Tempo médio de execução por agente e tamanho do mundo")
        plt.ylabel("Tempo médio (s)")
        plt.xlabel("Agente-Tamanho")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "grafico_tempo_medio.png"))
        plt.close()

    for metric in ["vitórias", "mortes", "sobreviveu"]:
        _desenhar(f"grafico_{metric}", lambda m=metric: barras(m), relatorio)
    _desenhar("grafico_tempo_medio", tempo_medio, relatorio)
    return relatorio


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


def gerar_graficos_avancados(dados_extra, output_dir):
    """
    Gera gráficos avançados a partir dos dados extras coletados durante as execuções.
    Cada gráfico é salvo na pasta de saída. Os dados esperados devem estar em arrays/listas.
    Gráficos sem dados suficientes são pulados e falhas não interrompem os demais (#37).
    :return: dict com os nomes em "gerados", "pulados" e "falhas"
    """
    relatorio = _relatorio_vazio()

    memoria, cpu = _serie(dados_extra, 'memoria'), _serie(dados_extra, 'cpu')
    fitness = _serie(dados_extra, 'fitness')
    fitness_pop = _matriz(dados_extra, 'fitness_pop')  # shape: (gerações, população)
    fitness_final = _serie(dados_extra, 'fitness_final')
    diversidade = _matriz(dados_extra, 'diversidade_vars')  # shape: (gerações, variáveis)
    pop_final = _matriz(dados_extra, 'pop_final')  # shape: (indivíduos, genes)

    # 1. Memória + CPU + Distribuição dos Recursos ao longo do tempo
    def memoria_cpu():
        plt.figure(figsize=(10,5))
        plt.plot(memoria, label='Memória (MB)')
        plt.plot(cpu, label='CPU (%)')
        plt.title('Uso de Memória e CPU durante Execução')
        plt.xlabel('Iteração')
        plt.ylabel('Uso')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "memoria_cpu.png"))
        plt.close()

    # 2. Evolução do Fitness (convergência) ao longo das gerações
    def evolucao_fitness():
        plt.figure(figsize=(8,5))
        plt.plot(fitness)
        plt.title('Evolução do Fitness (Convergência)')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "evolucao_fitness.png"))
        plt.close()

    # 3. Comportamento de Convergência da População (mínimo, médio e máximo de fitness)
    def convergencia_populacao():
        plt.figure(figsize=(8,5))
        plt.plot(np.min(fitness_pop, axis=1), label='Mínimo')
        plt.plot(np.mean(fitness_pop, axis=1), label='Médio')
        plt.plot(np.max(fitness_pop, axis=1), label='Máximo')
        plt.title('Comportamento de Convergência da População')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "convergencia_populacao.png"))
        plt.close()

    # 4. Média das Curvas de Convergência com Desvio Padrão
    def curva_convergencia_std():
        mean = np.mean(fitness_pop, axis=1)
        std = np.std(fitness_pop, axis=1)
        plt.figure(figsize=(8,5))
        plt.plot(mean, label='Média')
        plt.fill_between(range(len(mean)), mean-std, mean+std, alpha=0.3, label='Desvio Padrão')
        plt.title('Média das Curvas de Convergência com Desvio Padrão')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "curva_convergencia_std.png"))
        plt.close()

    # 5. Plot do Violino para distribuição do fitness por geração
    def violin_fitness():
        plt.figure(figsize=(8,5))
        sns.violinplot(data=fitness_pop.T)
        plt.title('Distribuição do Fitness por Geração (Violin Plot)')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "violin_fitness.png"))
        plt.close()

    # 6. Função de Distribuição Acumulada (ECDF) do fitness final
    def ecdf_fitness_final():
        plt.figure(figsize=(8,5))
        sns.ecdfplot(fitness_final)
        plt.title('Função de Distribuição Acumulada do Fitness Final')
        plt.xlabel('Fitness')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "ecdf_fitness_final.png"))
        plt.close()

    # 7. Mapa de Calor da Diversidade por Variável ao longo das gerações
    def heatmap_diversidade():
        plt.figure(figsize=(10,6))
        sns.heatmap(diversidade, cmap='viridis')
        plt.title('Mapa de Calor da Diversidade por Variável')
        plt.xlabel('Variável')
        plt.ylabel('Geração')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "heatmap_diversidade.png"))
        plt.close()

    # 8. Gráfico de Área Empilhada da Diversidade por Variável
    def area_empilhada_diversidade():
        plt.figure(figsize=(10,6))
        # Cada linha de diversidade_vars é uma geração, cada coluna uma variável
        plt.stackplot(range(diversidade.shape[0]), diversidade.T)
        plt.title('Área Empilhada da Diversidade por Variável')
        plt.xlabel('Geração')
        plt.ylabel('Diversidade')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "area_empilhada_diversidade.png"))
        plt.close()

    # 9. PCA para Visualizar Agrupamentos Genéticos da população final
    def pca_populacao_final():
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(pop_final)
        plt.figure(figsize=(8,6))
        plt.scatter(X_pca[:,0], X_pca[:,1], alpha=0.7)
        plt.title('PCA dos Indivíduos da População Final')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "pca_populacao_final.png"))
        plt.close()

    # Cada gráfico com a condição para existir: com dados insuficientes, ele é pulado
    graficos = [
        ("memoria_cpu", memoria_cpu, memoria is not None and cpu is not None),
        ("evolucao_fitness", evolucao_fitness, fitness is not None),
        ("convergencia_populacao", convergencia_populacao, fitness_pop is not None),
        ("curva_convergencia_std", curva_convergencia_std, fitness_pop is not None),
        ("violin_fitness", violin_fitness, fitness_pop is not None),
        ("ecdf_fitness_final", ecdf_fitness_final, fitness_final is not None),
        ("heatmap_diversidade", heatmap_diversidade, diversidade is not None),
        ("area_empilhada_diversidade", area_empilhada_diversidade, diversidade is not None),
        # O PCA de 2 componentes precisa de pelo menos 2 indivíduos e 2 genes
        ("pca_populacao_final", pca_populacao_final, pop_final is not None and min(pop_final.shape) >= 2),
    ]
    for nome, funcao, tem_dados in graficos:
        if tem_dados:
            _desenhar(nome, funcao, relatorio)
        else:
            relatorio["pulados"].append(nome)

    if relatorio["pulados"]:
        print(f"ℹ️ Gráficos pulados por falta de dados: {', '.join(relatorio['pulados'])}")
    return relatorio
