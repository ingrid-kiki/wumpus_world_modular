# ==============================
# ga/individual.py
# ==============================
import random

def random_action():
    # Retorna uma ação aleatória válida para o agente
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT', 'GRAB', 'SHOOT'])

class Individual:
    def __init__(self, chrom_length):
        # Inicializa o cromossomo com uma sequência aleatória de ações
        self.chromosome = [random_action() for _ in range(chrom_length)]
        # Valor de fitness (avaliação de desempenho do indivíduo)
        self.fitness = None

    def evaluate(self, world):
        """
        Executa a sequência de ações no mundo e avalia o desempenho.
        """
        temp_world = world.clone()  # Cria uma cópia do mundo para simulação
        score = 0  # Inicializa a pontuação
        for action in self.chromosome:
            # Executa cada ação do cromossomo no mundo simulado
            percept, status = temp_world.step(action)
            if status == 'DEAD':
                # Penalidade alta se o agente morrer
                score -= 100
                break
            if 'GLITTER' in percept:
                # Bônus se encontrar o ouro
                score += 100
            # Penalidade por cada ação executada (para incentivar soluções curtas)
            score -= 1
        # Salva o fitness final do indivíduo
        self.fitness = score

