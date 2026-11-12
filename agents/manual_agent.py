# ==============================
# agents/manual_agent.py
# ==============================
"""
# Este arquivo implementa o ManualAgent, um agente controlado manualmente pelo usuário
# via terminal no ambiente Wumpus World. O agente solicita comandos de ação ao usuário
# a cada passo, permitindo interação direta e didática com o ambiente. Ideal para fins
# educacionais, testes e comparação com agentes automáticos do projeto.
"""

from agents.agente import Agente
from world.constantes import ACOES


class ManualAgent(Agente):
    def run(self):
        """
        Agente controlado manualmente pelo usuário via terminal.
        Recebe comandos de ação e interage com o ambiente passo a passo.
        """
        # Continua enquanto o jogo não termina (vitória ou morte)
        while not self.world.is_done():
            # Solicita ao usuário uma ação via terminal
            while True:
                action = input("Ação (CIMA, BAIXO, ESQUERDA, DIREITA, AGARRAR, TIRO): ").strip().upper()
                if action in ACOES:
                    break
                print(f"❌ Ação inválida: '{action}'. Tente novamente.")

            # Executa a ação no ambiente e registra o passo
            perception, status = self.world.step(action)
            self.registrar_passo(action, perception, status)
            print(f"[Passo {len(self.historico)}] Ação: {action} | Percepção: {perception} | Status: {status}")
        return self.resultado()
