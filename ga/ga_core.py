# ==============================
# ga/ga_core.py
# ==============================
# Este arquivo implementa o núcleo do algoritmo genético utilizado pelo GeneticAgent
# no projeto Wumpus World. Define a classe GeneticAlgorithm, responsável por criar,
# evoluir e selecionar populações de indivíduos (soluções), aplicando operadores de
# seleção, cruzamento e mutação para buscar sequências de ações que maximizem o desempenho
# do agente no ambiente. Serve como base para experimentos de IA evolutiva no projeto.

import copy
import random
import psutil
import os
import numpy as np

# Importa a classe Individual (representa um possível agente/solução)
from .individual import Individual

class GeneticAlgorithm:
    def __init__(self, pop_size, gens, chrom_length, mutation_rate=0.02, crossover_rate=0.5):
        # Tamanho da população de indivíduos
        self.pop_size = pop_size
        # Número de gerações (iterações do algoritmo)
        self.gens = gens
        # Tamanho do cromossomo (quantidade de ações em cada indivíduo)
        self.chrom_length = chrom_length
        # Taxa de mutação padrão
        self.mutation_rate = mutation_rate
        # Taxa de cruzamento padrão
        self.crossover_rate = crossover_rate
        # Histórico do fitness médio, máximo e mínimo por geração
        self.fitness_history = []  # Lista de dicionários: {'min': x, 'mean': y, 'max': z}
        # Histórico do fitness de toda a população por geração (para gráficos avançados)
        self.fitness_pop = []
        # Histórico de uso de memória por geração
        self.memory_history = []
        # Histórico de uso de CPU por geração
        self.cpu_history = []
        # Diversidade de genes por posição no cromossomo
        self.diversidade_history = []

    def run(self, world, logger=None):
        # Registra o uso de memória e CPU antes de iniciar as gerações
        process = psutil.Process(os.getpid())
        process.cpu_percent()

        # Cria a população inicial de indivíduos aleatórios
        population = [Individual(self.chrom_length) for _ in range(self.pop_size)]
        for g in range(self.gens):
            # Uso de memória em MB
            memory_mb = process.memory_info().rss / (1024 * 1024)
            self.memory_history.append(memory_mb)
            # Uso de CPU em porcentagem
            self.cpu_history.append(process.cpu_percent())
            
            # Avalia o fitness de cada indivíduo na população
            for ind in population:
                ind.evaluate(world)

            # Ordena a população do melhor para o pior fitness
            population.sort(key=lambda x: x.fitness, reverse=True)

            diversidade_geracao = []
            # Para cada posição no cromossomo (cada variável)
            for i in range(self.chrom_length):
                # Encontra o número de genes únicos nessa posição em toda a população
                genes_na_posicao = set(ind.chromosome[i] for ind in population)
                diversidade_geracao.append(len(genes_na_posicao))
            self.diversidade_history.append(diversidade_geracao)

            # Coleta estatísticas de fitness para gráficos
            fitness_vals = [ind.fitness for ind in population]
            self.fitness_history.append({
                'min': min(fitness_vals),
                'mean': sum(fitness_vals) / len(fitness_vals),
                'max': max(fitness_vals)
            })
            self.fitness_pop.append(fitness_vals.copy())

            # Logging da geração
            if logger:
                logger.write(f"[GA] Geração {g+1}: min={min(fitness_vals)}, mean={sum(fitness_vals)/len(fitness_vals):.2f}, max={max(fitness_vals)}")
            
            # Elitismo: mantém os dois melhores indivíduos da geração atual
            next_gen = population[:2]
            
            # Preenche o restante da próxima geração com cruzamento e mutação
            while len(next_gen) < self.pop_size:
                # Seleciona dois pais para cruzamento
                p1, p2 = self.select(population), self.select(population)
                # Verifica se a taxa de cruzamento é atingida
                if random.random() < self.crossover_rate:
                    # Realiza o cruzamento (crossover) para gerar dois filhos
                    c1, c2 = self.crossover(p1, p2)
                else:
                    # Se não cruzar, copia os pais diretamente
                    c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)

                # Aplica mutação nos filhos
                self.mutate(c1)
                self.mutate(c2)
                # Adiciona os filhos à próxima geração
                next_gen.extend([c1, c2])
            
            # Atualiza a população para a próxima geração
            population = next_gen[:self.pop_size]  # Garante tamanho correto

        # Avalia todos da última geração (caso tenha novos filhos não avaliados)
        for ind in population:
            if ind.fitness is None:
                ind.evaluate(world)

        # Salva o melhor indivíduo encontrado
        best_individual = max(population, key=lambda x: x.fitness)
        best_individual_fitness = best_individual.fitness
        final_population_chromosomes = [ind.chromosome for ind in population]

        # Logging final
        if logger:
            logger.write(f"[GA] Fim das gerações. Melhor fitness: {best_individual_fitness}")
        
        return {
            "best": best_individual,
            "fitness_history": self.fitness_history,
            "fitness_pop": self.fitness_pop,
            "final_pop": final_population_chromosomes,
            "memoria": self.memory_history,
            "cpu": self.cpu_history,
            "diversidade_vars": np.array(self.diversidade_history)
        }

    def select(self, population):
        # Seleciona aleatoriamente um indivíduo entre os 10 melhores (elitismo/seleção por torneio)
        return copy.deepcopy(random.choice(population[:10]))

    def crossover(self, p1, p2):
        # Realiza o cruzamento de dois pais para gerar dois filhos
        point = random.randint(1, self.chrom_length - 1)  # Ponto de corte aleatório
        c1 = Individual(self.chrom_length)
        c2 = Individual(self.chrom_length)
        # Combina partes dos cromossomos dos pais para formar os filhos
        c1.chromosome = p1.chromosome[:point] + p2.chromosome[point:]
        c2.chromosome = p2.chromosome[:point] + p1.chromosome[point:]
        return c1, c2

    def mutate(self, individual):
        for i in range(self.chrom_length):
            # Aplica mutação com base na taxa de mutação
            if random.random() < self.mutation_rate:
                individual.chromosome[i] = self.random_action()
        
    def random_action(self):
        # Gera uma ação aleatória válida para o cromossomo
        return random.choice(['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA', 'AGARRAR', 'TIRO'])
