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

def random_action():
    # Retorna uma ação aleatória válida para o agente
    return random.choice(['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA', 'AGARRAR', 'TIRO'])

class Individual:
    def __init__(self, chrom_length):
        # Inicializa o cromossomo com uma sequência aleatória de ações
        self.chromosome = [random_action() for _ in range(chrom_length)]
        # Valor de fitness (avaliação de desempenho do indivíduo)
        self.fitness = None

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
            if action == 'TIRO' and 'FEDOR' in percept:
                score += 25   # Atirar com cheiro = tentativa válida
            if action in ['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA']:
                score -= 0.5  # Penalidade leve por andar
            else:
                score -= 1  # Penalidade padrão

        # Pequeno bônus por sobrevivência
        if temp_world.is_alive:
            score += 10
        # Salva o fitness final do indivíduo
        self.fitness = score


