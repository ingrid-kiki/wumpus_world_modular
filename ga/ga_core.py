# ==============================
# ga/ga_core.py
# ==============================
# Este arquivo implementa o núcleo do algoritmo genético utilizado pelo GeneticAgent
# no projeto Wumpus World. Define a classe GeneticAlgorithm, responsável por criar,
# evoluir e selecionar populações de indivíduos (soluções), aplicando operadores de
# seleção, cruzamento e mutação para buscar sequências de ações que maximizem o desempenho
# do agente no ambiente. Serve como base para experimentos de IA evolutiva no projeto.

import os
import random

import numpy as np
import psutil

# Importa a classe Individual (representa um possível agente/solução)
from world.constantes import ACOES

from .individual import Individual

ELITE = 2  # os melhores indivíduos passam intactos para a próxima geração
CANDIDATOS_A_PAI = 10  # a seleção sorteia os pais entre os melhores desta quantidade
BYTES_POR_MB = 1024 * 1024


class GeneticAlgorithm:
    def __init__(self, pop_size, gens, chrom_length, mutation_rate, crossover_rate, seed=None, proximidade=0.0):
        # Gerador próprio, para o AG ser reprodutível sem depender do random global (#23)
        self.rng = random.Random(seed)
        # Peso do bônus de proximidade ao ouro no fitness; 0 mantém o fitness original (#31)
        self.proximidade = proximidade
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
        # Cache de fitness por cromossomo: o mundo não muda durante a evolução, então o mesmo
        # cromossomo tem sempre a mesma nota. Não altera o resultado, só evita simular de novo.
        self._cache_fitness = {}
        self.avaliacoes = 0  # simulações realmente executadas
        self.acertos_cache = 0  # avaliações respondidas pelo cache

    def avaliar(self, individual, world):
        """Define individual.fitness, simulando só cromossomos ainda não vistos."""
        chave = tuple(individual.chromosome)
        if chave in self._cache_fitness:
            individual.fitness = self._cache_fitness[chave]
            self.acertos_cache += 1
        else:
            individual.evaluate(world, self.proximidade)
            self._cache_fitness[chave] = individual.fitness
            self.avaliacoes += 1

    def run(self, world):
        """Evolui a população por `gens` gerações no mundo dado e devolve o melhor indivíduo e os históricos."""
        # Cada execução começa com o cache vazio (o cache vale para um mundo só)
        self._cache_fitness = {}
        self.avaliacoes = 0
        self.acertos_cache = 0
        # Registra o uso de memória e CPU antes de iniciar as gerações
        processo = psutil.Process(os.getpid())
        processo.cpu_percent()

        # Cria a população inicial de indivíduos aleatórios
        population = [Individual(self.chrom_length, self.rng) for _ in range(self.pop_size)]
        for _ in range(self.gens):
            self._registrar_recursos(processo)
            # Avalia o fitness de cada indivíduo e ordena do melhor para o pior
            for ind in population:
                self.avaliar(ind, world)
            population.sort(key=lambda x: x.fitness, reverse=True)
            self._registrar_geracao(population)
            population = self._proxima_geracao(population)

        # Avalia todos da última geração (caso tenha novos filhos não avaliados)
        for ind in population:
            if ind.fitness is None:
                self.avaliar(ind, world)
        best_individual = max(population, key=lambda x: x.fitness)
        return self._resultado(best_individual, population)

    def _registrar_recursos(self, processo):
        """Guarda o uso de memória (MB) e de CPU (%) no início de uma geração."""
        self.memory_history.append(processo.memory_info().rss / BYTES_POR_MB)
        self.cpu_history.append(processo.cpu_percent())

    def _registrar_geracao(self, population):
        """Guarda a diversidade de genes por posição e o fitness da população já ordenada."""
        # Quantos genes diferentes há em cada posição do cromossomo, em toda a população
        diversidade_geracao = [len({ind.chromosome[i] for ind in population}) for i in range(self.chrom_length)]
        self.diversidade_history.append(diversidade_geracao)

        fitness_vals = [ind.fitness for ind in population]
        self.fitness_history.append(
            {"min": min(fitness_vals), "mean": sum(fitness_vals) / len(fitness_vals), "max": max(fitness_vals)}
        )
        self.fitness_pop.append(fitness_vals.copy())

    def _proxima_geracao(self, population):
        """Elitismo, seleção, cruzamento e mutação: monta a próxima geração a partir da atual, já ordenada."""
        next_gen = population[:ELITE]  # os melhores passam intactos
        while len(next_gen) < self.pop_size:
            p1, p2 = self.select(population), self.select(population)
            if self.rng.random() < self.crossover_rate:
                c1, c2 = self.crossover(p1, p2)
            else:
                c1, c2 = p1.copia(), p2.copia()  # sem cruzamento, os filhos são cópias dos pais
            self.mutate(c1)
            self.mutate(c2)
            next_gen.extend([c1, c2])
        return next_gen[: self.pop_size]  # o último par pode passar do tamanho

    def _resultado(self, best_individual, population):
        """Resultado de run(): o melhor indivíduo, a população final e os históricos para os gráficos."""
        return {
            "best": best_individual,
            "fitness_history": self.fitness_history,
            "fitness_pop": self.fitness_pop,
            "final_pop": [ind.chromosome for ind in population],
            "memoria": self.memory_history,
            "cpu": self.cpu_history,
            "diversidade_vars": np.array(self.diversidade_history),
            "avaliacoes": self.avaliacoes,
            "acertos_cache": self.acertos_cache,
        }

    def select(self, population):
        # Seleciona aleatoriamente um indivíduo entre os 10 melhores (seleção por truncamento)
        return self.rng.choice(population[:CANDIDATOS_A_PAI]).copia()

    def crossover(self, p1, p2):
        # Realiza o cruzamento de dois pais para gerar dois filhos
        if self.chrom_length < 2:  # com um gene só não há ponto de corte possível (#38)
            return p1.copia(), p2.copia()
        point = self.rng.randint(1, self.chrom_length - 1)  # Ponto de corte aleatório
        c1 = Individual(0)
        c2 = Individual(0)
        # Combina partes dos cromossomos dos pais para formar os filhos
        c1.chromosome = p1.chromosome[:point] + p2.chromosome[point:]
        c2.chromosome = p2.chromosome[:point] + p1.chromosome[point:]
        return c1, c2

    def mutate(self, individual):
        mudou = False
        for i in range(self.chrom_length):
            # Aplica mutação com base na taxa de mutação
            if self.rng.random() < self.mutation_rate:
                individual.chromosome[i] = self.random_action()
                mudou = True
        if mudou:
            # O cromossomo mudou: o fitness herdado do pai não vale mais (#19)
            individual.fitness = None

    def random_action(self):
        # Gera uma ação aleatória válida para o cromossomo
        return self.rng.choice(ACOES)
