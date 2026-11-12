# ==============================
# visual/visualizer.py
# ==============================
"""
# Janela gráfica (pygame) que reproduz, passo a passo, uma partida já jogada.
#
# O main.py a oferece no fim das execuções únicas (opções 2, 3 e 4 do menu). Ela recebe uma
# cópia do mundo no estado inicial e o histórico do agente, e refaz as ações nessa cópia: a
# janela mostra exatamente o que aconteceu, sem rodar o agente de novo. Cada casa mostra as
# percepções de quem estivesse nela; o Wumpus, os poços, o ouro e o agente aparecem com cores
# próprias, e os avisos de grito, morte e vitória ficam no canto de cima.
"""

import pygame

from world.constantes import BRILHO, BRISA, FEDOR

TAMANHO_DA_CASA = 100  # pixels
PASSOS_POR_SEGUNDO = 2
CORES = {
    "fundo": (255, 255, 255),
    "casa": (200, 200, 200),
    "borda": (0, 0, 0),
    "wumpus": (255, 0, 0),
    "poco": (100, 100, 100),
    "ouro": (255, 215, 0),
    "agente": (0, 255, 0),
    "alerta": (255, 0, 0),
    "vitoria": (0, 128, 0),
}
# A fonte padrão do pygame não tem emojis: as percepções aparecem por extenso
NOMES_DAS_PERCEPCOES = ((BRISA, "brisa"), (FEDOR, "fedor"), (BRILHO, "brilho"))


class Visualizer:
    def __init__(self, world, cell_size=TAMANHO_DA_CASA):
        """Abre a janela do tamanho do mundo. `world` é o mundo que será desenhado e alterado na reprodução."""
        pygame.init()
        self.world = world
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((world.size * cell_size, world.size * cell_size))
        pygame.display.set_caption("Wumpus World")
        self.font = pygame.font.SysFont(None, 24)
        self.fonte_pequena = pygame.font.SysFont(None, 20)
        self.clock = pygame.time.Clock()

    def draw_cell(self, x, y, color, text=None):
        """Pinta a casa (x, y), com borda e um texto opcional no canto."""
        rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, CORES["borda"], rect, 2)
        if text:
            self.screen.blit(self.font.render(text, True, CORES["borda"]), (rect.x + 10, rect.y + 10))

    def draw_world(self, passo=None):
        """Desenha o estado atual do mundo; `passo` é o item do histórico que levou até ele, se houver."""
        self.screen.fill(CORES["fundo"])
        self._desenhar_percepcoes()
        self._desenhar_elementos()
        self._desenhar_avisos(passo)
        pygame.display.flip()

    def _percepcao_na_casa(self, pos):
        """O que o agente perceberia na casa `pos`, sem mudar o mundo."""
        posicao_real = self.world.agent_pos
        self.world.agent_pos = pos
        percepcao = self.world.perceive()
        self.world.agent_pos = posicao_real
        return percepcao

    def _desenhar_percepcoes(self):
        """Cada casa com as percepções (brisa, fedor, brilho) que o agente teria nela."""
        for x in range(self.world.size):
            for y in range(self.world.size):
                self.draw_cell(x, y, CORES["casa"])
                percepcao = self._percepcao_na_casa((x, y))
                palavras = [nome for percebido, nome in NOMES_DAS_PERCEPCOES if percebido in percepcao]
                for linha, palavra in enumerate(palavras):
                    posicao = (y * self.cell_size + 10, x * self.cell_size + 40 + 18 * linha)
                    self.screen.blit(self.fonte_pequena.render(palavra, True, CORES["borda"]), posicao)

    def _desenhar_elementos(self):
        """Wumpus (enquanto vivo), poços, ouro e, por cima de tudo, o agente."""
        if self.world.wumpus_alive:
            self.draw_cell(*self.world.wumpus_pos, CORES["wumpus"], "W")
        for poco in self.world.pits:
            self.draw_cell(*poco, CORES["poco"], "P")
        self.draw_cell(*self.world.gold_pos, CORES["ouro"], "G")
        self.draw_cell(*self.world.agent_pos, CORES["agente"], "A")

    def _desenhar_avisos(self, passo):
        """O passo atual e os avisos de grito, morte e vitória, no canto de cima."""
        avisos = []
        if passo:
            avisos.append((f"Passo {passo['passo']}: {passo['acao']}", CORES["borda"]))
        if self.world.last_scream:
            avisos.append(("GRITO!", CORES["alerta"]))
        if not self.world.is_alive:
            avisos.append(("AGENTE MORTO!", CORES["alerta"]))
        if self.world.won:
            avisos.append(("VITÓRIA!", CORES["vitoria"]))
        for linha, (texto, cor) in enumerate(avisos):
            # Fundo branco atrás do texto, para ele não se misturar com as percepções da casa
            self.screen.blit(self.font.render(texto, True, cor, CORES["fundo"]), (10, 10 + 30 * linha))

    def reproduzir(self, historico, passos_por_segundo=PASSOS_POR_SEGUNDO, esperar_fechar=True):
        """
        Mostra o estado inicial e refaz, no mundo da janela, cada ação do histórico.
        Ao fim, espera a pessoa fechar a janela (a menos que `esperar_fechar` seja False).
        :return: quantos passos foram mostrados
        """
        self.draw_world()
        mostrados, fechada = 0, False
        for passo in historico:
            if self._fechou():
                fechada = True
                break
            self.clock.tick(passos_por_segundo)
            self.world.step(passo["acao"])
            self.draw_world(passo)
            mostrados += 1
        if esperar_fechar and not fechada:
            self._esperar_fechar()
        pygame.quit()
        return mostrados

    def _fechou(self):
        """True se a pessoa fechou a janela."""
        return any(evento.type == pygame.QUIT for evento in pygame.event.get())

    def _esperar_fechar(self):
        while not self._fechou():
            self.clock.tick(10)
