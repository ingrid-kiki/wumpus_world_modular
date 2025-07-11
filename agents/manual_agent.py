# Estrutura Modular Comentada do Projeto Wumpus_ERAD_ERAMIA_2021

# ==============================
# agents/manual_agent.py
# ==============================
class ManualAgent:
    def __init__(self, world):
        # Recebe uma referência ao ambiente (mundo do Wumpus)
        self.world = world

    def run(self):
        """
        Agente controlado manualmente pelo usuário via terminal.
        Recebe comandos de ação e interage com o ambiente passo a passo.
        """
        step = 1  # Inicializa o contador de passos
        # Continua enquanto o jogo não termina (vitória ou morte)
        while not self.world.is_done():
            # Solicita ao usuário uma ação via terminal
            action = input("Ação (UP, DOWN, LEFT, RIGHT, GRAB, SHOOT): ")
            # Executa a ação no ambiente e recebe percepção e status
            perception, status = self.world.step(action)
            # Exibe informações do passo atual
            print(f"[Passo {step}] Ação: {action} | Percepção: {perception} | Status: {status}")
            step += 1  # Incrementa


