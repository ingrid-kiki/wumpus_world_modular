# agents/logic_knowledge_base.py

class LogicKnowledgeBase:
    def __init__(self):
        self.perceptions = []

    def infer_action(self, perception):
        """
        Método simples de inferência para fins didáticos.
        Retorna uma ação baseada na percepção atual.
        """
        self.perceptions.append(perception)

        # Exemplo básico: se sentir brilho (GLITTER), tenta pegar o ouro
        if 'GLITTER' in perception:
            return 'GRAB'
        elif 'STENCH' in perception:
            return 'SHOOT'
        elif 'BREEZE' in perception:
            return 'LEFT'
        else:
            return 'RIGHT'
