# ==============================
# agents/manual_agent.py
# ==============================
"""
# Este arquivo implementa o AgenteManual, um agente controlado manualmente pelo usuário
# via terminal no ambiente Wumpus World. O agente solicita comandos de ação ao usuário
# a cada passo, permitindo interação direta e didática com o ambiente. Ideal para fins
# educacionais, testes e comparação com agentes automáticos do projeto.
"""

from agents.agente import Agente
from world.constantes import ACOES


class AgenteManual(Agente):
    def executar(self):
        """
        Agente controlado manualmente pelo usuário via terminal.
        Recebe comandos de ação e interage com o ambiente passo a passo.
        """
        # Continua enquanto o jogo não termina (vitória ou morte)
        while not self.mundo.terminou():
            # Solicita ao usuário uma ação via terminal
            while True:
                acao = input("Ação (CIMA, BAIXO, ESQUERDA, DIREITA, AGARRAR, TIRO): ").strip().upper()
                if acao in ACOES:
                    break
                print(f"❌ Ação inválida: '{acao}'. Tente novamente.")

            # Executa a ação no ambiente e registra o passo
            percepcao, status = self.mundo.agir(acao)
            self.registrar_passo(acao, percepcao, status)
            print(f"[Passo {len(self.historico)}] Ação: {acao} | Percepção: {percepcao} | Status: {status}")
        return self.resultado()
