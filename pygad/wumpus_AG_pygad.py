# Wumpus_GeneticAlgorithm.py (Modificado para usar PyGAD)

import numpy as np
import time
import pickle
import matplotlib.pyplot
from WumpsimAG import WumpusWorld
import ga_pygad  # <--- ALTERAÇÃO: Importa o novo módulo

# Parâmetros do ambiente e do algoritmo genético
size_world = 6           # Tamanho do mundo Wumpus (6x6)
size_chromo = 200        # Tamanho do cromossomo (quantidade de ações)
size_pop = 100           # Tamanho da população
num_parents_mating = 2   # Número de pais para crossover (PyGAD gerencia o resto)
num_generations = 100    # Número de gerações
crossover_probability = 0.5
mutation_probability = 0.15
tournament_number = 3    # Número de indivíduos no torneio de seleção
elit_ratio = 0.02        # Proporção de elitismo
min_gene = 0             # Valor mínimo de gene (ação)
max_gene = 6             # Valor máximo de gene (ação)

# Parâmetros de execução dos testes
tests = 10               # Quantidade de testes por mundo
worlds = 5               # Quantidade de mundos diferentes
seeds = [43, 44, 45, 46, 50] # Sementes para geração dos mundos

# Dicionário para armazenar resultados dos testes
results = {'fitness':[], 'test':[], 'world':[], 'gold':[], 'death_wumpus':[], 'win':[], 'alive':[], 'cromo':[]}

inicio = time.time()     # Marca o tempo inicial da execução

# Loop principal: para cada mundo
for world in range(worlds):
    wumpus_world = None  # Mundo aleatório a cada iteração
    # Para cada teste dentro do mundo
    for test in range(tests):
        print(f"Iniciando Teste {test+1}/{tests} para o Mundo {world+1}/{worlds}...")

        # ALTERAÇÃO: Agrupa os parâmetros para passar para a nova função do PyGAD
        ga_params = {
            'num_generations': num_generations,
            'size_pop': size_pop,
            'size_chromo': size_chromo,
            'num_parents_mating': num_parents_mating,
            'crossover_probability': crossover_probability,
            'mutation_probability': mutation_probability,
            'tournament_number': tournament_number,
            'elit_ratio': elit_ratio,
            'min_gene': min_gene,
            'max_gene': max_gene,
            'wumpus_world': wumpus_world,
            'seed': seeds[world]
        }

        # --- ALTERAÇÃO: O laço de evolução manual foi substituído por esta única chamada ---
        best_outputs, best_cromo, best_current_state = ga_pygad.solve_with_pygad(ga_params)
        # ------------------------------------------------------------------------------------

        # ALTERAÇÃO: PyGAD maximiza o fitness (maior = melhor), então usamos argmax
        idx = np.argmax(best_outputs) # iteração com a melhor solução

        print('Melhor Fitness em todas gerações: ')
        print(best_outputs[idx])

        print('Objetivos alcançados:')
        print(f"[Ouro, Wumpus Morto, Vitória, Vivo] = {best_current_state[idx]}")
        print("-" * 30)

        # Salva resultados do melhor indivíduo do teste
        results['fitness'].append(best_outputs[idx])
        results['test'].append(test)
        results['world'].append(world)
        results['gold'].append(best_current_state[idx][0])
        results['death_wumpus'].append(best_current_state[idx][1])
        results['win'].append(best_current_state[idx][2])
        results['alive'].append(best_current_state[idx][3])
        results['cromo'].append(best_cromo[idx])

# Salva os resultados em arquivo para análise posterior
# Certifique-se de que a pasta 'results' existe
filename = 'results/AG_PyGAD_dict_6x6_e6.pkl'
outfile = open(filename, 'wb')
pickle.dump(results, outfile)
outfile.close()
print(f"\nResultados salvos em: {filename}")

# Exibe o tempo total de execução
print(f"Tempo total de execução: {time.time() - inicio:.2f} segundos")

# O código para plotar os gráficos pode ser usado para visualizar a convergência.
# Lembre-se que agora a curva de fitness deve ser ascendente (maior é melhor).
# Exemplo de como plotar o melhor fitness ao longo das gerações do último teste:
matplotlib.pyplot.plot(best_outputs)
matplotlib.pyplot.xlabel("Geração")
matplotlib.pyplot.ylabel("Fitness (Pontuação)")
matplotlib.pyplot.title("Melhor Fitness por Geração (Último Teste)")
matplotlib.pyplot.grid(True)
matplotlib.pyplot.show()
