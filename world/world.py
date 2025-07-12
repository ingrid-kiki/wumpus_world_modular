# ==============================
# world/world.py
# ==============================
'''
# Este arquivo implementa a classe World, responsável por representar e gerenciar o ambiente
# do Wumpus World. O ambiente inclui o agente, o ouro, o Wumpus e os poços, além das regras
# de movimentação, percepções e interações. Fornece métodos para executar ações, simular
# percepções, verificar condições de vitória/morte e clonar o estado do mundo para simulações
# do algoritmo genético e testes dos agentes inteligentes do projeto.
'''

import random
import copy

class World:
    def __init__(self, size, seed=None):
        """
        Inicializa o mundo do Wumpus.
        :param size: Tamanho do mundo (quadrado size x size)
        :param seed: Semente para geração aleatória (opcional)
        """
        self.size = size
        if seed is not None:
            random.seed(seed)  # Define a semente para resultados reproduzíveis
        
        # Elementos do mundo
        self.agent_pos = (0, 0)  # Posição inicial do agente
        self.gold_pos = self.random_pos(exclude=[self.agent_pos])  # Posição do ouro
        self.wumpus_pos = self.random_pos(exclude=[self.agent_pos, self.gold_pos])  # Posição do Wumpus
        # Lista de posições dos poços, evitando sobreposição com agente, ouro e Wumpus
        self.pits = [self.random_pos(exclude=[self.agent_pos, self.gold_pos, self.wumpus_pos]) for _ in range(size // 2)]

        self.is_alive = True         # Estado de vida do agente
        self.wumpus_alive = True     # Estado de vida do Wumpus
        self.last_scream = False     # Indica se o último tiro matou o Wumpus
        self.won = False             # Indica se o agente venceu

    def random_pos(self, exclude=[]):
        """
        Gera uma posição aleatória no mundo, excluindo as posições fornecidas.
        :param exclude: Lista de posições a serem evitadas
        :return: Tupla (x, y) com a posição sorteada
        """
        while True:
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if pos not in exclude:
                return pos

    def step(self, action):
        """
            Executa uma ação no ambiente: movimento + interação.
            :param action: Ação a ser executada ('CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA', 'AGARRAR', 'TIRO')
            :return: (percepção, status) onde status pode ser 'OK', 'MORTO' ou 'GANHOU'
        """
        self.last_scream = False  # Reset do grito
        self.move_agent(action)   # Movimento separado
        status = self.interact(action)  # Interações separadas
        return self.perceive(), status

    def move_agent(self, action):
        """
        Move o agente no grid se a ação for de movimento.
        """
        x, y = self.agent_pos
        if action == 'CIMA' and x > 0:
            self.agent_pos = (x - 1, y)
        elif action == 'BAIXO' and x < self.size - 1:
            self.agent_pos = (x + 1, y)
        elif action == 'ESQUERDA' and y > 0:
            self.agent_pos = (x, y - 1)
        elif action == 'DIREITA' and y < self.size - 1:
            self.agent_pos = (x, y + 1)

    def interact(self, action):
        """
        Aplica os efeitos da ação (pegar ouro, atirar, morrer etc.).
        :return: status final da jogada
        """
        # Ouro
        if action == 'AGARRAR' and self.agent_pos == self.gold_pos:
            self.won = True
            return 'GANHOU'

        # Tiro no Wumpus
        if action == 'TIRO':
            if self.is_adjacent(self.agent_pos, self.wumpus_pos) and self.wumpus_alive:
                self.wumpus_alive = False
                self.last_scream = True

        # Morte por Wumpus
        if self.agent_pos == self.wumpus_pos and self.wumpus_alive:
            self.is_alive = False
            return 'MORTO'

        # Morte por poço
        if self.agent_pos in self.pits:
            self.is_alive = False
            return 'MORTO'

        # Vitória
        if self.won:
            return 'GANHOU'

        return 'OK'


    def perceive(self):
        """
        Retorna as percepções do agente na posição atual.
        :return: Lista de percepções ('FEDOR', 'BRISA', 'BRILHO')
        """
        percept = []
        x, y = self.agent_pos

        # Verifica células adjacentes para FEDOR (Wumpus) e BRISA (poço)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if (nx, ny) == self.wumpus_pos and self.wumpus_alive:
                    percept.append('FEDOR')
                if (nx, ny) in self.pits:
                    percept.append('BRISA')

        # Verifica se está sobre o ouro
        if self.agent_pos == self.gold_pos:
            percept.append('BRILHO')

        return percept

    def is_done(self):
        """
        Verifica se o jogo terminou (vitória ou morte).
        :return: True se terminou, False caso contrário
        """
        return self.won or not self.is_alive

    def clone(self):
        """
        Retorna uma cópia profunda do mundo (útil para simulações).
        :return: Novo objeto World idêntico ao atual
        """
        return copy.deepcopy(self)

    def is_adjacent(self, pos1, pos2):
        """
        Verifica se duas posições são adjacentes (cima, baixo, esquerda, direita).
        :param pos1: Primeira posição (x, y)
        :param pos2: Segunda posição (x, y)
        :return: True se adjacentes, False caso contrário
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)
