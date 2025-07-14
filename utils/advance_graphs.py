# ==============================
# utils/graficos.py
# ==============================
'''
# Este módulo centraliza todas as funções de geração de gráficos do projeto Wumpus World.
# Ele inclui funções para criar gráficos básicos (barras, tempo médio) e avançados
# (memória/CPU, evolução do fitness, convergência, violino, ECDF, mapas de calor,
# área empilhada e PCA) a partir dos dados coletados nos benchmarks dos agentes.
# Todos os gráficos são salvos automaticamente nas pastas de saída organizadas por execução.
'''

import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
import numpy as np

def gerar_graficos(df, output_dir):
    """
    Gera gráficos básicos de barras para vitórias, mortes, sobrevivências e tempo médio.
    Salva cada gráfico na pasta de saída especificada.
    """
    # Gera gráficos de barras para vitórias, mortes e sobrevivências
    for metric in ["vitórias", "mortes", "sobreviveu"]:
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
        print(f"Salvando gráfico em: {os.path.join(output_dir, f'grafico_{metric}.png')}")
        plt.close()

    # Gráfico de barras para o tempo médio de execução por agente e tamanho
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
    print(f"Salvando gráfico em: {os.path.join(output_dir, 'grafico_tempo_medio.png')}")
    plt.close()

def gerar_graficos_avancados(dados_extra, output_dir):
    """
    Gera gráficos avançados a partir dos dados extras coletados durante as execuções.
    Cada gráfico é salvo na pasta de saída. Os dados esperados devem estar em arrays/listas.
    """

    # DEBUG: Mostra informações sobre os dados recebidos e o diretório
    print("=== [DEBUG] gerar_graficos_avancados ===")
    print(f"output_dir recebido: {output_dir}")
    print(f"Diretório existe? {os.path.exists(output_dir)}")
    print(f"Chaves em dados_extra: {list(dados_extra.keys())}")
    for k, v in dados_extra.items():
        print(f"  - {k}: tipo={type(v)}, tamanho={len(v)}")
        if isinstance(v, np.ndarray):
            print(f"    shape: {v.shape}")
        elif isinstance(v, list) and v and hasattr(v[0], 'shape'):
            print(f"    shape do primeiro elemento: {v[0].shape}")

    # 1. Memória + CPU + Distribuição dos Recursos ao longo do tempo
    if 'memoria' in dados_extra and 'cpu' in dados_extra:
        plt.figure(figsize=(10,5))
        plt.plot(dados_extra['memoria'], label='Memória (MB)')
        plt.plot(dados_extra['cpu'], label='CPU (%)')
        plt.title('Uso de Memória e CPU durante Execução')
        plt.xlabel('Iteração')
        plt.ylabel('Uso')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "memoria_cpu.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'memoria_cpu.png')}")
        plt.close()

    # 2. Evolução do Fitness (convergência) ao longo das gerações
    if 'fitness' in dados_extra:
        plt.figure(figsize=(8,5))
        # Se for lista de listas, transforme em array 2D
        if isinstance(dados_extra['fitness'][0], list):
            fitness_array = np.array(dados_extra['fitness'])
            # Agora você pode plotar cada linha como uma execução
            for idx, fitness_list in enumerate(fitness_array):
                plt.plot(fitness_list, label=f"Execução {idx+1}")
        else:
            plt.plot(dados_extra['fitness'])
        plt.title('Evolução do Fitness (Convergência)')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "evolucao_fitness.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'evolucao_fitness.png')}")
        plt.close()

    # 3. Comportamento de Convergência da População (mínimo, médio e máximo de fitness)
    if 'fitness_pop' in dados_extra:
        fitness_pop = np.array(dados_extra['fitness_pop'])  # shape: (gerações, população)
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
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'convergencia_populacao.png')}")
        plt.close()

    # 4. Média das Curvas de Convergência com Desvio Padrão
    if 'fitness_pop' in dados_extra:
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
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'curva_convergencia_std.png')}")
        plt.close()

    # 5. Plot do Violino para distribuição do fitness por geração
    if 'fitness_pop' in dados_extra:
        plt.figure(figsize=(8,5))
        sns.violinplot(data=fitness_pop.T)
        plt.title('Distribuição do Fitness por Geração (Violin Plot)')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "violin_fitness.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'violin_fitness.png')}")
        plt.close()

    # 6. Função de Distribuição Acumulada (ECDF) do fitness final
    if 'fitness_final' in dados_extra:
        plt.figure(figsize=(8,5))
        sns.ecdfplot(dados_extra['fitness_final'])
        plt.title('Função de Distribuição Acumulada do Fitness Final')
        plt.xlabel('Fitness')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "ecdf_fitness_final.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'ecdf_fitness_final.png')}")
        plt.close()

    # 7. Mapa de Calor da Diversidade por Variável ao longo das gerações
    if 'diversidade_vars' in dados_extra:
        plt.figure(figsize=(10,6))
        sns.heatmap(dados_extra['diversidade_vars'], cmap='viridis')
        plt.title('Mapa de Calor da Diversidade por Variável')
        plt.xlabel('Variável')
        plt.ylabel('Geração')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "heatmap_diversidade.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'heatmap_diversidade.png')}")
        plt.close()

    # 8. Gráfico de Área Empilhada da Diversidade por Variável
    if 'diversidade_vars' in dados_extra:
        plt.figure(figsize=(10,6))
        # Cada linha de diversidade_vars é uma geração, cada coluna uma variável
        plt.stackplot(range(dados_extra['diversidade_vars'].shape[0]), 
                      dados_extra['diversidade_vars'].T)
        plt.title('Área Empilhada da Diversidade por Variável')
        plt.xlabel('Geração')
        plt.ylabel('Diversidade')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "area_empilhada_diversidade.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'area_empilhada_diversidade.png')}")
        plt.close()

    # 9. PCA para Visualizar Agrupamentos Genéticos da população final
    if 'pop_final' in dados_extra:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(dados_extra['pop_final'])
        plt.figure(figsize=(8,6))
        plt.scatter(X_pca[:,0], X_pca[:,1], alpha=0.7)
        plt.title('PCA dos Indivíduos da População Final')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "pca_populacao_final.png"))
        print(f"Salvando gráfico em: {os.path.join(output_dir, 'pca_populacao_final.png')}")
        plt.close()

    # 10. Histórico de Fitness por Execução (avançado)
    if 'fitness' in dados_extra and len(dados_extra['fitness']) > 0:
        fitness_data = dados_extra['fitness']
        if isinstance(fitness_data[0], list):
            fitness_data = np.array(fitness_data)
            for idx, f in enumerate(fitness_data):
                plt.plot(f, label=f"Execução {idx+1}")
            plt.title("Histórico de Fitness por Execução")
            plt.xlabel("Geração")
            plt.ylabel("Fitness")
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "fitness_avancado.png"))
            plt.close()
        else:
            # Caso seja lista simples
            plt.plot(fitness_data)
            plt.title("Histórico de Fitness")
            plt.xlabel("Geração")
            plt.ylabel("Fitness")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "fitness_avancado.png"))
            plt.close()

    # Gráfico de teste simples (para verificar salvamento)
    plt.figure()
    plt.plot([1,2,3], [4,5,6])
    plt.title("Teste de Salvamento")
    plt.savefig(os.path.join(output_dir, "grafico_teste.png"))
    print(f"Salvando gráfico em: {os.path.join(output_dir, 'grafico_teste.png')}")
    plt.close()

    # Verifica se os gráficos principais foram salvos (exemplo de asserção)
    assert os.path.exists(os.path.join(output_dir, "grafico_vitórias.png")), "Gráfico de vitórias não foi salvo!"
    assert os.path.exists(os.path.join(output_dir, "grafico_mortes.png")), "Gráfico de mortes não foi salvo!"
    assert os.path.exists(os.path.join(output_dir, "grafico_sobreviveu.png")), "Gráfico de sobrevivências não foi salvo!"
    assert os.path.exists(os.path.join(output_dir, "grafico_tempo_medio.png")), "Gráfico de tempo médio não foi salvo!"

# Removido o bloco que usa 'output_dir' fora de contexto.
# Certifique-se de passar 'output_dir' corretamente ao chamar as funções deste módulo.
