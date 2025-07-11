import pygame
import sys
import time

class Visualizer:
    def __init__(self, world):
        # Inicializa o Pygame
        pygame.init()
        # Referência ao mundo do Wumpus
        self.world = world
        # Tamanho de cada célula do grid (em pixels)
        self.cell_size = 100
        # Cria a janela do Pygame com tamanho proporcional ao mundo
        self.screen = pygame.display.set_mode((world.size * self.cell_size, world.size * self.cell_size))
        # Define o título da janela
        pygame.display.set_caption("Wumpus World Viewer")
        # Fonte para desenhar textos nas células
        self.font = pygame.font.SysFont(None, 24)
        # Relógio para controlar o FPS da visualização
        self.clock = pygame.time.Clock()

    def draw_cell(self, x, y, color, text=None):
        # Desenha uma célula na posição (x, y) com a cor especificada
        rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)
        # Desenha a borda da célula
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        # Se houver texto, desenha o texto na célula
        if text:
            label = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(label, (rect.x + 10, rect.y + 10))

    def draw_world(self):
        # Preenche o fundo da tela de branco
        self.screen.fill((255, 255, 255))

        # 🧱 Desenha todas as células básicas do grid
        for x in range(self.world.size):
            for y in range(self.world.size):
                self.draw_cell(x, y, (200, 200, 200))

        # 🟥 Desenha o Wumpus (se estiver vivo)
        if hasattr(self.world, "wumpus_alive") and self.world.wumpus_alive and hasattr(self.world, "wumpus_pos"):
            x, y = self.world.wumpus_pos
            self.draw_cell(x, y, (255, 0, 0), "W")

        # 🕳️ Desenha os poços
        if hasattr(self.world, "pits"):
            for x, y in self.world.pits:
                self.draw_cell(x, y, (100, 100, 100), "P")

        # 🟡 Desenha o ouro
        if hasattr(self.world, "gold_pos"):
            x, y = self.world.gold_pos
            self.draw_cell(x, y, (255, 215, 0), "G")

        # 🟢 Desenha o agente
        if hasattr(self.world, "agent_pos"):
            x, y = self.world.agent_pos
            self.draw_cell(x, y, (0, 255, 0), "A")

        # 📣 Exibe o grito do Wumpus se ele morreu
        if hasattr(self.world, "last_scream") and self.world.last_scream:
            scream_label = self.font.render("SCREAM!", True, (255, 0, 0))
            self.screen.blit(scream_label, (10, 10))

        # ☠️ Exibe mensagem de morte do agente
        if hasattr(self.world, "is_alive") and not self.world.is_alive:
            death_label = self.font.render("AGENTE MORTO!", True, (255, 0, 0))
            self.screen.blit(death_label, (10, 40))

        # 🏆 Exibe mensagem de vitória
        if hasattr(self.world, "won") and self.world.won:
            win_label = self.font.render("VITÓRIA!", True, (0, 128, 0))
            self.screen.blit(win_label, (10, 70))

        # Atualiza a tela com todos os desenhos
        pygame.display.flip()

    def run(self):
        # Loop principal da visualização
        running = True
        while running:
            # Desenha o mundo a cada frame
            self.draw_world()
            # Processa eventos do Pygame (como fechar a janela)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Controla a taxa de atualização (FPS)
            self.clock.tick(5)
        # Encerra o Pygame e o programa
        pygame.quit()
        sys.exit()
