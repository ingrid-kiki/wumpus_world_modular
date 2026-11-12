# ==============================
# ga/individual.py
# ==============================
"""
# Este arquivo implementa a classe Individuo, que representa um possível agente/solução
# para o algoritmo genético no Wumpus World. Cada indivíduo possui um cromossomo (sequência
# de ações) e um valor de fitness, avaliado ao simular sua execução no ambiente. Serve como
# unidade básica de evolução para o AlgoritmoGenetico, permitindo experimentos de IA evolutiva.
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


def acao_aleatoria(gerador=random):
    # Retorna uma ação aleatória válida para o agente
    return gerador.choice(ACOES)


def _distancia(pos, alvo):
    """Distância em passos (horizontais e verticais) entre duas casas."""
    return abs(pos[0] - alvo[0]) + abs(pos[1] - alvo[1])


def _pontuar_acao(pontuacao, acao, percepcao, mundo):
    """Soma à pontuação os pontos de uma ação que não matou o agente, na mesma ordem de sempre."""
    if acao == AGARRAR and BRILHO in percepcao:
        pontuacao += BONUS_OURO  # Bônus se encontrar o ouro
    if acao == TIRO and mundo.grito:
        # Bônus por matar o Wumpus (o mundo registra o grito). Antes a condição era
        # 'FEDOR' na percepção pós-tiro, que nunca acontece: o fedor some quando ele morre (#21)
        pontuacao += BONUS_WUMPUS
    if acao in ACOES_DE_MOVIMENTO:
        pontuacao -= CUSTO_MOVIMENTO  # Penalidade leve por andar
    else:
        pontuacao -= CUSTO_OUTRA_ACAO  # Penalidade padrão
    return pontuacao


class Individuo:
    def __init__(self, tamanho_cromossomo, gerador=None):
        # Gerador aleatório do AG (ou o módulo random, se não for informado)
        gerador = gerador if gerador is not None else random
        # Inicializa o cromossomo com uma sequência aleatória de ações
        self.cromossomo = [acao_aleatoria(gerador) for _ in range(tamanho_cromossomo)]
        # Valor de fitness (avaliação de desempenho do indivíduo)
        self.fitness = None

    def copia(self):
        """Cópia independente do cromossomo, mantendo o fitness (mais rápida que copy.deepcopy)."""
        novo = Individuo(0)
        novo.cromossomo = list(self.cromossomo)
        novo.fitness = self.fitness
        return novo

    def avaliar(self, mundo, proximidade=0.0):
        """
        Executa a sequência de ações no mundo e avalia o desempenho.
        :param mundo: Instância do mundo do Wumpus para simulação
        :param proximidade: Peso do bônus por chegar perto do ouro. Com 0 (padrão), o fitness é o
                            original; com peso positivo, soma de 0 a `proximidade` conforme a menor
                            distância até o ouro alcançada na sequência (#31)
        :return: Nenhum retorno, mas atualiza o atributo fitness do indivíduo
        """
        mundo_simulado = mundo.clonar()  # Cria uma cópia do mundo para simulação
        pontuacao = 0  # Inicializa a pontuação
        menor_distancia = _distancia(mundo_simulado.posicao_agente, mundo.posicao_ouro)
        for acao in self.cromossomo:
            # Executa cada ação do cromossomo no mundo simulado
            percepcao, status = mundo_simulado.agir(acao)
            menor_distancia = min(menor_distancia, _distancia(mundo_simulado.posicao_agente, mundo.posicao_ouro))
            if status == MORTO:
                pontuacao -= PENALIDADE_MORTE  # Penalidade alta se o agente morrer
                break
            pontuacao = _pontuar_acao(pontuacao, acao, percepcao, mundo_simulado)
            if status == GANHOU:
                # O jogo acabou: as ações restantes do cromossomo não contam (#20)
                break

        # Pequeno bônus por sobrevivência
        if mundo_simulado.agente_vivo:
            pontuacao += BONUS_SOBREVIVENCIA
        # Sinal de progresso até o ouro: sem ele, a pontuação é quase plana até pegar o ouro (#31)
        if proximidade:
            distancia_maxima = 2 * (mundo.tamanho - 1)  # de um canto do mundo ao canto oposto
            pontuacao += proximidade * (1 - menor_distancia / distancia_maxima)
        # Salva o fitness final do indivíduo
        self.fitness = pontuacao
