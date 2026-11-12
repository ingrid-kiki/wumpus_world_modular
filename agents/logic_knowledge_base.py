# ==============================
# agents/logic_knowledge_base.py
# ==============================
"""
# Este arquivo implementa a classe BaseConhecimento, responsável por manter e atualizar
# a base de conhecimento lógica do agente simbólico no Wumpus World. Ela armazena percepções,
# estados conhecidos do ambiente e escolhe a próxima ação com regras simples. A marca "seguro" é
# registrada, mas a decisão não a consulta: o agente logico_seguro (agents/logico_seguro.py) faz isso.
# Serve como núcleo de raciocínio lógico para o AgenteLogico, facilitando decisões baseadas em regras.
"""

from world.constantes import AGARRAR, BRILHO, BRISA, DESLOCAMENTOS, DIREITA, FEDOR, TIRO

MOVIMENTOS = [(dx, dy, acao) for acao, (dx, dy) in DESLOCAMENTOS.items()]  # ordem: cima, baixo, esquerda, direita


class BaseConhecimento:
    def __init__(self, tamanho=None):
        # Tamanho do grid: sem ele, a KB "anda" para fora do mapa e entra em loop (#18)
        self.tamanho = tamanho
        self.percepcoes = []
        self.conhecidas = {}  # (x, y) -> {'seguro': bool, 'visitado': bool, 'percepcoes': [...]}
        self.visitas = {}  # (x, y) -> número de vezes que o agente esteve na célula
        self.posicao_atual = (0, 0)

    def dentro_do_mundo(self, pos):
        """True se a posição está dentro do grid (ou se o tamanho é desconhecido)."""
        if self.tamanho is None:
            return True
        x, y = pos
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho

    def vizinhas_validas(self):
        """Vizinhas válidas da posição atual, na ordem CIMA, BAIXO, ESQUERDA, DIREITA."""
        x, y = self.posicao_atual
        for dx, dy, acao in MOVIMENTOS:
            pos = (x + dx, y + dy)
            if self.dentro_do_mundo(pos):
                yield pos, acao

    def atualizar_conhecimento(self, percepcao):
        x, y = self.posicao_atual
        self.conhecidas[(x, y)] = {
            "seguro": BRISA not in percepcao and FEDOR not in percepcao,
            "visitado": True,
            "percepcoes": percepcao,
        }
        self.visitas[(x, y)] = self.visitas.get((x, y), 0) + 1
        self.percepcoes.append((x, y, percepcao))

    def inferir_acao(self, percepcao):
        """
        Método simples de inferência para fins didáticos.
        Retorna uma ação baseada na percepção atual.
        """
        self.atualizar_conhecimento(percepcao)
        # Exemplo básico: se sentir brilho, tenta pegar o ouro
        if BRILHO in percepcao:
            return AGARRAR
        if FEDOR in percepcao:
            return TIRO

        vizinhas = list(self.vizinhas_validas())
        # Exploração simples: andar para uma vizinha ainda não visitada
        for pos, acao in vizinhas:
            if pos not in self.conhecidas:
                return acao

        # Todas as vizinhas já foram visitadas: volta pela menos visitada (empate: ordem de MOVIMENTOS).
        # Antes o fallback era sempre 'DIREITA', que deixava o agente parado na borda direita.
        if vizinhas:
            _, acao = min(vizinhas, key=lambda item: self.visitas.get(item[0], 0))
            return acao
        return DIREITA

    def atualizar_posicao(self, acao, nova_posicao=None):
        """
        Atualiza a posição da KB. Se o mundo informar a posição real (nova_posicao), ela é usada;
        assim um movimento bloqueado pela parede não dessincroniza a KB (#18).
        """
        if nova_posicao is not None:
            self.posicao_atual = tuple(nova_posicao)
            return
        x, y = self.posicao_atual
        dx, dy = DESLOCAMENTOS.get(acao, (0, 0))
        destino = (x + dx, y + dy)
        if self.dentro_do_mundo(destino):
            self.posicao_atual = destino
