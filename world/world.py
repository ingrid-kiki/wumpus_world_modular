# ==============================
# world/world.py
# ==============================
"""
# Este arquivo implementa a classe Mundo, responsável por representar e gerenciar o ambiente
# do Wumpus World. O ambiente inclui o agente, o ouro, o Wumpus e os poços, além das regras
# de movimentação, percepções e interações. Fornece métodos para executar ações, simular
# percepções, verificar condições de vitória/morte e clonar o estado do mundo para simulações
# do algoritmo genético e testes dos agentes inteligentes do projeto.
"""

import copy
import random

from world.constantes import AGARRAR, BRILHO, BRISA, DESLOCAMENTOS, FEDOR, GANHOU, MORTO, OK, TIRO

TAMANHO_MINIMO = 2


class Mundo:
    def __init__(self, tamanho, semente=None):
        """
        Inicializa o mundo do Wumpus.
        :param tamanho: Tamanho do mundo (quadrado tamanho x tamanho)
        :param semente: Semente para geração aleatória (opcional)
        """
        # Abaixo disso não cabem agente, ouro, Wumpus e poços, e posicao_aleatoria() nunca terminaria (#38)
        if tamanho < TAMANHO_MINIMO:
            raise ValueError(f"O mundo precisa ter tamanho {TAMANHO_MINIMO} ou maior (recebido: {tamanho}).")
        self.tamanho = tamanho
        self.semente = semente
        # Gerador próprio: não altera o random global (#23)
        self.gerador = random.Random(semente)

        # Elementos do mundo
        self.posicao_agente = (0, 0)  # Posição inicial do agente
        self.posicao_ouro = self.posicao_aleatoria(excluir=[self.posicao_agente])  # Posição do ouro
        self.posicao_wumpus = self.posicao_aleatoria(
            excluir=[self.posicao_agente, self.posicao_ouro]
        )  # Posição do Wumpus
        # Lista de posições dos poços: sem repetir casa e sem cair no agente, no ouro ou no Wumpus (#22)
        self.pocos = []
        for _ in range(tamanho // 2):
            ocupadas = [self.posicao_agente, self.posicao_ouro, self.posicao_wumpus, *self.pocos]
            self.pocos.append(self.posicao_aleatoria(excluir=ocupadas))

        self.agente_vivo = True  # Estado de vida do agente
        self.wumpus_vivo = True  # Estado de vida do Wumpus
        self.grito = False  # Indica se o último tiro matou o Wumpus
        self.ganhou = False  # Indica se o agente venceu

    def posicao_aleatoria(self, excluir=None):
        """
        Gera uma posição aleatória no mundo, excluindo as posições fornecidas.
        :param excluir: Lista de posições a serem evitadas
        :return: Tupla (x, y) com a posição sorteada
        """
        excluir = excluir or []
        while True:
            pos = (self.gerador.randint(0, self.tamanho - 1), self.gerador.randint(0, self.tamanho - 1))
            if pos not in excluir:
                return pos

    def agir(self, acao):
        """
        Executa uma ação no ambiente: movimento + interação.
        :param acao: Ação a ser executada ('CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA', 'AGARRAR', 'TIRO')
        :return: (percepção, status) onde status pode ser 'OK', 'MORTO' ou 'GANHOU'
        """
        self.grito = False  # Reset do grito
        # Depois de vencer ou morrer, nenhuma ação tem efeito (#20)
        if self.terminou():
            return self.perceber(), (GANHOU if self.ganhou else MORTO)
        self.mover_agente(acao)  # Movimento separado
        status = self.interagir(acao)  # Interações separadas
        return self.perceber(), status

    def mover_agente(self, acao):
        """
        Move o agente no grid se a ação for de movimento.
        """
        dx, dy = DESLOCAMENTOS.get(acao, (0, 0))  # ações que não são movimento não deslocam
        x, y = self.posicao_agente[0] + dx, self.posicao_agente[1] + dy
        if 0 <= x < self.tamanho and 0 <= y < self.tamanho:  # contra a parede, o agente fica onde está
            self.posicao_agente = (x, y)

    def interagir(self, acao):
        """
        Aplica os efeitos da ação (pegar ouro, atirar, morrer etc.).
        :return: status final da jogada
        """
        # Ouro
        if acao == AGARRAR and self.posicao_agente == self.posicao_ouro:
            self.ganhou = True
            return GANHOU

        # Tiro no Wumpus
        if acao == TIRO and self.adjacentes(self.posicao_agente, self.posicao_wumpus) and self.wumpus_vivo:
            self.wumpus_vivo = False
            self.grito = True

        # Morte por Wumpus
        if self.posicao_agente == self.posicao_wumpus and self.wumpus_vivo:
            self.agente_vivo = False
            return MORTO

        # Morte por poço
        if self.posicao_agente in self.pocos:
            self.agente_vivo = False
            return MORTO

        # Vitória
        if self.ganhou:
            return GANHOU

        return OK

    def perceber(self):
        """
        Retorna as percepções do agente na posição atual.
        :return: Lista de percepções ('FEDOR', 'BRISA', 'BRILHO')
        """
        percepcao = []
        x, y = self.posicao_agente

        # Verifica células adjacentes para FEDOR (Wumpus) e BRISA (poço)
        for dx, dy in DESLOCAMENTOS.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                if (nx, ny) == self.posicao_wumpus and self.wumpus_vivo:
                    percepcao.append(FEDOR)
                if (nx, ny) in self.pocos:
                    percepcao.append(BRISA)

        # Verifica se está sobre o ouro
        if self.posicao_agente == self.posicao_ouro:
            percepcao.append(BRILHO)

        return percepcao

    def terminou(self):
        """
        Verifica se o jogo terminou (vitória ou morte).
        :return: True se terminou, False caso contrário
        """
        return self.ganhou or not self.agente_vivo

    def clonar(self):
        """
        Retorna uma cópia independente do mundo (útil para simulações).
        As posições são tuplas (imutáveis), então basta copiar os atributos e a lista de poços.
        O gerador aleatório é compartilhado: ele só é usado na criação do mundo.
        Antes era um copy.deepcopy, que respondia por ~70% do tempo do AG.
        :return: Novo objeto Mundo idêntico ao atual
        """
        novo = copy.copy(self)
        novo.pocos = list(self.pocos)
        return novo

    def adjacentes(self, pos_a, pos_b):
        """
        Verifica se duas posições são adjacentes (cima, baixo, esquerda, direita).
        :param pos_a: Primeira posição (x, y)
        :param pos_b: Segunda posição (x, y)
        :return: True se adjacentes, False caso contrário
        """
        x1, y1 = pos_a
        x2, y2 = pos_b
        return (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)
