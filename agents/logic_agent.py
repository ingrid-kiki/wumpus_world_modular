# ==============================
# agents/logic_agent.py
# ==============================
from agents.logic_knowledge_base import LogicKnowledgeBase

class LogicAgent:
    def __init__(self, world):
        # Referência ao ambiente (mundo do Wumpus)
        self.world = world
        # Base de conhecimento lógica para inferências
        self.knowledge = LogicKnowledgeBase()
        # Histórico das percepções do agente a cada passo
        self.perception_history = []
        self.logger = None  # Será injetado pelo main
    

    def run(self):
        """
        Executa o ciclo de vida do agente lógico.
        Atualiza a base de conhecimento e decide ações seguras.
        """
        passo = 1  # Contador de passos do agente
        # Continua enquanto o jogo não termina (vitória ou morte)
        while not self.world.is_done():
            # Obtém percepções do ambiente na posição atual
            perception = self.world.perceive()
            
            # Salva percepção no histórico para análise posterior
            self.perception_history.append({
                "passo": passo,
                "perception": perception
            })

            # Exibe percepção atual
            print(f"[Passo {passo}] Percepção: {perception}")
            
            # Decide próxima ação com base na percepção
            action = self.decide(perception)
            
            # Exibe ação escolhida
            print(f"[Passo {passo}] Ação decidida: {action}")
            
            # Executa ação no mundo e recebe novo status
            _, status = self.world.step(action)
            
            # Atualiza a posição atual na base de conhecimento
            self.knowledge.update_position(action)
            
            # Registra tudo no logger, se ele existir
            if self.logger:
                self.logger.write(f"[Passo {passo}] Percepção: {perception}")
                self.logger.write(f"[Passo {passo}] Ação decidida: {action}")
                self.logger.write(f"[Passo {passo}] Status: {status}\n")

            
            # Exibe status do agente após a ação no terminal
            print(f"[Passo {passo}] Status do agente: {status}\n")
            passo += 1  # Incrementa o passo
    
        # Exibe o histórico completo de percepções ao final
        print("📝 Histórico de percepções:")
        for item in self.perception_history:
            print(f"Passo {item['passo']}: {item['perception']}")


    def decide(self, perception):
        """
        Aplica a lógica simbólica do agente baseada nas percepções recebidas.
        Retorna a próxima ação lógica a ser executada.
        """
        return self.knowledge.infer_action(perception)
