# ==============================
# ga/ga_core.py
# ==============================
import copy
import random

from .individual import Individual  # Importa a classe Individual (representa um possível agente/solução)

class GeneticAlgorithm:
    def __init__(self, pop_size, gens, chrom_length):
        # Tamanho da população de indivíduos
        self.pop_size = pop_size
        # Número de gerações (iterações do algoritmo)
        self.gens = gens
        # Tamanho do cromossomo (quantidade de ações em cada indivíduo)
        self.chrom_length = chrom_length

    def run(self, world):
        # Cria a população inicial de indivíduos aleatórios
        population = [Individual(self.chrom_length) for _ in range(self.pop_size)]
        # Executa o algoritmo genético por um número fixo de gerações
        for g in range(self.gens):
            # Avalia o fitness de cada indivíduo na população
            for ind in population:
                ind.evaluate(world)
            # Ordena a população do melhor para o pior fitness
            population.sort(key=lambda x: x.fitness, reverse=True)
            # Elitismo: mantém os dois melhores indivíduos da geração atual
            next_gen = population[:2]
            # Preenche o restante da próxima geração com cruzamento e mutação
            while len(next_gen) < self.pop_size:
                # Seleciona dois pais para cruzamento
                p1, p2 = self.select(population), self.select(population)
                # Realiza o cruzamento (crossover) para gerar dois filhos
                c1, c2 = self.crossover(p1, p2)
                # Aplica mutação nos filhos
                self.mutate(c1)
                self.mutate(c2)
                # Adiciona os filhos à próxima geração
                next_gen.extend([c1, c2])
            # Atualiza a população para a próxima geração
            population = next_gen
        # Retorna o melhor indivíduo da população final        
        # Avalia todos da última geração (caso tenha novos filhos não avaliados)
        for ind in population:
            if ind.fitness is None:
                ind.evaluate(world)

        return max(population, key=lambda x: x.fitness)

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
        # Aplica mutação em um gene aleatório do cromossomo do indivíduo
        index = random.randint(0, self.chrom_length - 1)
        individual.chromosome[index] = self.random_action()
        
    def random_action(self):
        # Gera uma ação aleatória válida para o cromossomo
        # Exemplo: se as ações são inteiros de 0 a 3
        return random.choice(['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA', 'AGARRAR', 'TIRO'])


