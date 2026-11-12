# ==============================
# ga/individual.py
# ==============================
"""
# Este arquivo implementa a classe Individual, que representa um possível agente/solução
# para o algoritmo genético no Wumpus World. Cada indivíduo possui um cromossomo (sequência
# de ações) e um valor de fitness, avaliado ao simular sua execução no ambiente. Serve como
# unidade básica de evolução para o GeneticAlgorithm, permitindo experimentos de IA evolutiva.
"""

import random

from world.constantes import ACOES, ACOES_DE_MOVIMENTO, AGARRAR, BRILHO, GANHOU, MORTO, TIRO

# Pontos do fitness (ver docs/arquitetura/fluxo-ag.md)
PENALIDADE_MORTE = 100
BONUS_OURO = 100
BONUS_WUMPUS = 25
CUSTO_MOVIMENTO = 0.5
CUSTO_OUTRA_ACAO = 1
BONUS_SOBREVIVENCIA = 10


def random_action(rng=random):
    # Retorna uma ação aleatória válida para o agente
    return rng.choice(ACOES)


def _distancia(pos, alvo):
    """Distância em passos (horizontais e verticais) entre duas casas."""
    return abs(pos[0] - alvo[0]) + abs(pos[1] - alvo[1])


def _pontuar_acao(score, action, percept, mundo):
    """Soma à pontuação os pontos de uma ação que não matou o agente, na mesma ordem de sempre."""
    if action == AGARRAR and BRILHO in percept:
        score += BONUS_OURO  # Bônus se encontrar o ouro
    if action == TIRO and mundo.last_scream:
        # Bônus por matar o Wumpus (o mundo registra o grito). Antes a condição era
        # 'FEDOR' na percepção pós-tiro, que nunca acontece: o fedor some quando ele morre (#21)
        score += BONUS_WUMPUS
    if action in ACOES_DE_MOVIMENTO:
        score -= CUSTO_MOVIMENTO  # Penalidade leve por andar
    else:
        score -= CUSTO_OUTRA_ACAO  # Penalidade padrão
    return score


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

    def evaluate(self, world, proximidade=0.0):
        """
        Executa a sequência de ações no mundo e avalia o desempenho.
        :param world: Instância do mundo do Wumpus para simulação
        :param proximidade: Peso do bônus por chegar perto do ouro. Com 0 (padrão), o fitness é o
                            original; com peso positivo, soma de 0 a `proximidade` conforme a menor
                            distância até o ouro alcançada na sequência (#31)
        :return: Nenhum retorno, mas atualiza o atributo fitness do indivíduo
        """
        temp_world = world.clone()  # Cria uma cópia do mundo para simulação
        score = 0  # Inicializa a pontuação
        menor_distancia = _distancia(temp_world.agent_pos, world.gold_pos)
        for action in self.chromosome:
            # Executa cada ação do cromossomo no mundo simulado
            percept, status = temp_world.step(action)
            menor_distancia = min(menor_distancia, _distancia(temp_world.agent_pos, world.gold_pos))
            if status == MORTO:
                score -= PENALIDADE_MORTE  # Penalidade alta se o agente morrer
                break
            score = _pontuar_acao(score, action, percept, temp_world)
            if status == GANHOU:
                # O jogo acabou: as ações restantes do cromossomo não contam (#20)
                break

        # Pequeno bônus por sobrevivência
        if temp_world.is_alive:
            score += BONUS_SOBREVIVENCIA
        # Sinal de progresso até o ouro: sem ele, a pontuação é quase plana até pegar o ouro (#31)
        if proximidade:
            distancia_maxima = 2 * (world.size - 1)  # de um canto do mundo ao canto oposto
            score += proximidade * (1 - menor_distancia / distancia_maxima)
        # Salva o fitness final do indivíduo
        self.fitness = score
