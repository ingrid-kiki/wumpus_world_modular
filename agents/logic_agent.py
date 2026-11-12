# ==============================
# agents/logic_agent.py
# ==============================
"""
# Este arquivo implementa o LogicAgent, um agente inteligente para o Wumpus World
# baseado em lógica simbólica. O agente utiliza uma base de conhecimento lógica
# para decidir cada ação com regras simples a partir das percepções do ambiente, atualizando seu
# conhecimento a cada passo. O histórico dos passos é registrado para análise,
# e o agente pode integrar-se ao sistema de logs e benchmarks do projeto.
"""

from agents.agente import Agente
from agents.logic_knowledge_base import LogicKnowledgeBase

PASSOS_POR_CASA = 4  # limite de passos: 4 vezes o número de casas do mundo (#18)


class LogicAgent(Agente):
    def __init__(self, world, max_steps=None):
        super().__init__(world)
        # Base de conhecimento lógica para inferências; conhece o tamanho do grid (#18)
        self.knowledge = LogicKnowledgeBase(size=world.size)
        # Limite de passos: garante que run() sempre termina (#18)
        self.max_steps = max_steps if max_steps is not None else PASSOS_POR_CASA * world.size * world.size
        self.logger = None  # Será injetado pelo main

    def run(self):
        """
        Executa o ciclo de vida do agente lógico.
        Atualiza a base de conhecimento e decide a próxima ação com regras simples.
        """
        passo = 1  # Contador de passos do agente
        # Continua enquanto o jogo não termina (vitória ou morte) e há passos disponíveis
        while not self.world.is_done() and passo <= self.max_steps:
            # Obtém percepções do ambiente na posição atual
            perception = self.world.perceive()

            # Exibe percepção atual
            print(f"[Passo {passo}] Percepção: {perception}")

            # Decide próxima ação com base na percepção
            action = self.decide(perception)

            # Exibe ação escolhida
            print(f"[Passo {passo}] Ação decidida: {action}")

            # Executa ação no mundo e registra o passo
            percepcao_depois, status = self.world.step(action)
            self.registrar_passo(action, percepcao_depois, status)

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

        # Exibe o histórico completo ao final
        print("📝 Histórico:")
        for item in self.historico:
            print(f"Passo {item['passo']}: {item['acao']} -> {item['percepcao']}")

        return self.resultado()

    def decide(self, perception):
        """
        Aplica a lógica simbólica do agente baseada nas percepções recebidas.
        Retorna a próxima ação lógica a ser executada.
        """
        return self.knowledge.infer_action(perception)
