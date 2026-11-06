# ==============================
# agents/logic_agent.py
# ==============================
'''
# Este arquivo implementa o LogicAgent, um agente inteligente para o Wumpus World
# baseado em lógica simbólica. O agente utiliza uma base de conhecimento lógica
# para inferir ações seguras a partir das percepções do ambiente, atualizando seu
# conhecimento a cada passo. O histórico de percepções é registrado para análise,
# e o agente pode integrar-se ao sistema de logs e benchmarks do projeto.
'''

from agents.logic_knowledge_base import LogicKnowledgeBase

class LogicAgent:
    def __init__(self, world, max_steps=None):
        # Referência ao ambiente (mundo do Wumpus)
        self.world = world
        # Base de conhecimento lógica para inferências; conhece o tamanho do grid (#18)
        self.knowledge = LogicKnowledgeBase(size=world.size)
        # Limite de passos: garante que run() sempre termina (#18)
        self.max_steps = max_steps if max_steps is not None else 4 * world.size * world.size
        # Histórico das percepções do agente a cada passo
        self.perception_history = []
        self.logger = None  # Será injetado pelo main
    

    def run(self):
        """
        Executa o ciclo de vida do agente lógico.
        Atualiza a base de conhecimento e decide ações seguras.
        """
        passo = 1  # Contador de passos do agente
        # Continua enquanto o jogo não termina (vitória ou morte) e há passos disponíveis
        while not self.world.is_done() and passo <= self.max_steps:
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
            
            # Atualiza a posição na base de conhecimento com a posição real do mundo
            self.knowledge.update_position(action, self.world.agent_pos)
            
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

        return {"history": self.perception_history, "passos": passo - 1}


    def decide(self, perception):
        """
        Aplica a lógica simbólica do agente baseada nas percepções recebidas.
        Retorna a próxima ação lógica a ser executada.
        """
        return self.knowledge.infer_action(perception)
