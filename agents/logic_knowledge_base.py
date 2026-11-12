# ==============================
# agents/logic_knowledge_base.py
# ==============================
"""
# Este arquivo implementa a classe LogicKnowledgeBase, responsável por manter e atualizar
# a base de conhecimento lógica do agente simbólico no Wumpus World. Ela armazena percepções,
# estados conhecidos do ambiente e escolhe a próxima ação com regras simples. A marca "seguro" é
# registrada, mas a decisão não a consulta: o agente logico_seguro (agents/logico_seguro.py) faz isso.
# Serve como núcleo de raciocínio lógico para o LogicAgent, facilitando decisões baseadas em regras.
"""

from world.constantes import AGARRAR, BRILHO, BRISA, DESLOCAMENTOS, DIREITA, FEDOR, TIRO

MOVIMENTOS = [(dx, dy, acao) for acao, (dx, dy) in DESLOCAMENTOS.items()]  # ordem: cima, baixo, esquerda, direita


class LogicKnowledgeBase:
    def __init__(self, size=None):
        # Tamanho do grid: sem ele, a KB "anda" para fora do mapa e entra em loop (#18)
        self.size = size
        self.perceptions = []
        self.known = {}  # (x, y) -> {'seguro': bool, 'visitado': bool, 'percepções': [...]}
        self.visits = {}  # (x, y) -> número de vezes que o agente esteve na célula
        self.current_pos = (0, 0)

    def in_grid(self, pos):
        """True se a posição está dentro do grid (ou se o tamanho é desconhecido)."""
        if self.size is None:
            return True
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def neighbors(self):
        """Vizinhas válidas da posição atual, na ordem CIMA, BAIXO, ESQUERDA, DIREITA."""
        x, y = self.current_pos
        for dx, dy, action in MOVIMENTOS:
            pos = (x + dx, y + dy)
            if self.in_grid(pos):
                yield pos, action

    def update_knowledge(self, perception):
        x, y = self.current_pos
        self.known[(x, y)] = {
            "seguro": BRISA not in perception and FEDOR not in perception,
            "visitado": True,
            "percepções": perception,
        }
        self.visits[(x, y)] = self.visits.get((x, y), 0) + 1
        self.perceptions.append((x, y, perception))

    def infer_action(self, perception):
        """
        Método simples de inferência para fins didáticos.
        Retorna uma ação baseada na percepção atual.
        """
        self.update_knowledge(perception)
        # Exemplo básico: se sentir brilho, tenta pegar o ouro
        if BRILHO in perception:
            return AGARRAR
        if FEDOR in perception:
            return TIRO

        vizinhas = list(self.neighbors())
        # Exploração simples: andar para uma vizinha ainda não visitada
        for pos, action in vizinhas:
            if pos not in self.known:
                return action

        # Todas as vizinhas já foram visitadas: volta pela menos visitada (empate: ordem de MOVIMENTOS).
        # Antes o fallback era sempre 'DIREITA', que deixava o agente parado na borda direita.
        if vizinhas:
            _, action = min(vizinhas, key=lambda item: self.visits.get(item[0], 0))
            return action
        return DIREITA

    def update_position(self, action, new_pos=None):
        """
        Atualiza a posição da KB. Se o mundo informar a posição real (new_pos), ela é usada;
        assim um movimento bloqueado pela parede não dessincroniza a KB (#18).
        """
        if new_pos is not None:
            self.current_pos = tuple(new_pos)
            return
        x, y = self.current_pos
        dx, dy = DESLOCAMENTOS.get(action, (0, 0))
        destino = (x + dx, y + dy)
        if self.in_grid(destino):
            self.current_pos = destino
