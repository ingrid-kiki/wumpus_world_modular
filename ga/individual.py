# ==============================
# ga/individual.py
# ==============================
'''
# Este arquivo implementa a classe Individual, que representa um possível agente/solução
# para o algoritmo genético no Wumpus World. Cada indivíduo possui um cromossomo (sequência
# de ações) e um valor de fitness, avaliado ao simular sua execução no ambiente. Serve como
# unidade básica de evolução para o GeneticAlgorithm, permitindo experimentos de IA evolutiva.
'''

import random

def random_action(rng=random):
    # Retorna uma ação aleatória válida para o agente
    return rng.choice(['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA', 'AGARRAR', 'TIRO'])

class Individual:
    def __init__(self, chrom_length, rng=None):
        # Gerador aleatório do AG (ou o módulo random, se não for informado)
        rng = rng if rng is not None else random
        # Inicializa o cromossomo com uma sequência aleatória de ações
        self.chromosome = [random_action(rng) for _ in range(chrom_length)]
        # Valor de fitness (avaliação de desempenho do indivíduo)
        self.fitness = None

    def copia(self):
        """Cópia independente do cromossomo, mantendo o fitness (mais rápida que copy.deepcopy)."""
        novo = Individual(0)
        novo.chromosome = list(self.chromosome)
        novo.fitness = self.fitness
        return novo

    def evaluate(self, world):
        """
        Executa a sequência de ações no mundo e avalia o desempenho.
        :param world: Instância do mundo do Wumpus para simulação
        :return: Nenhum retorno, mas atualiza o atributo fitness do indivíduo
        """
        temp_world = world.clone()  # Cria uma cópia do mundo para simulação
        score = 0  # Inicializa a pontuação
        for i, action in enumerate(self.chromosome):
            # Executa cada ação do cromossomo no mundo simulado
            percept, status = temp_world.step(action)

            if status == 'MORTO':
                # Penalidade alta se o agente morrer
                score -= 100
                break
            if action == 'AGARRAR' and 'BRILHO' in percept:
                score += 100  # Bônus se encontrar o ouro
            if action == 'TIRO' and temp_world.last_scream:
                # Bônus por matar o Wumpus (o mundo registra o grito). Antes a condição era
                # 'FEDOR' na percepção pós-tiro, que nunca acontece: o fedor some quando ele morre (#21)
                score += 25
            if action in ['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA']:
                score -= 0.5  # Penalidade leve por andar
            else:
                score -= 1  # Penalidade padrão
            if status == 'GANHOU':
                # O jogo acabou: as ações restantes do cromossomo não contam (#20)
                break

        # Pequeno bônus por sobrevivência
        if temp_world.is_alive:
            score += 10
        # Salva o fitness final do indivíduo
        self.fitness = score


