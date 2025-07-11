# ==============================
# agents/logic_knowledge_base.py
# ==============================

class LogicKnowledgeBase:
    def __init__(self):
        self.perceptions = []
        self.known = {}  # (x, y) → {'safe': bool, 'visited': bool, 'perceptions': []}
        self.current_pos = (0, 0)

    def update_knowledge(self, perception):
        x, y = self.current_pos
        self.known[(x, y)] = {
            'seguro': 'BRISA' not in perception and 'FEDOR' not in perception,
            'visitado': True,
            'percepções': perception
        }
        self.perceptions.append((x, y, perception))

    def infer_action(self, perception):
        """
        Método simples de inferência para fins didáticos.
        Retorna uma ação baseada na percepção atual.
        """
        self.update_knowledge(perception)
        # Exemplo básico: se sentir brilho (GLITTER), tenta pegar o ouro
        if 'BRILHO' in perception:
            return 'AGARRAR'
        if 'FEDOR' in perception:
            return 'TIRO'

        # Exploração simples: andar para uma célula vizinha não visitada e provavelmente segura
        for dx, dy, action in [(-1, 0, 'CIMA'), (1, 0, 'BAIXO'), (0, -1, 'ESQUERDA'), (0, 1, 'DIREITA')]:
            nx, ny = self.current_pos[0] + dx, self.current_pos[1] + dy
            if (nx, ny) not in self.known:
                return action
            if self.known[(nx, ny)]['seguro'] and not self.known[(nx, ny)]['visitado']:
                return action

        # Falha segura: não achou caminho bom → tenta sair andando
        return 'DIREITA'

    def update_position(self, action):
        x, y = self.current_pos
        if action == 'CIMA':
            self.current_pos = (x - 1, y)
        elif action == 'BAIXO':
            self.current_pos = (x + 1, y)
        elif action == 'ESQUERDA':
            self.current_pos = (x, y - 1)
        elif action == 'DIREITA':
            self.current_pos = (x, y + 1)
