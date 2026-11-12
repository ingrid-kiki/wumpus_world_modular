# ==============================
# world/constantes.py
# ==============================
"""
# Constantes das regras do Wumpus World: ações, percepções e status de uma jogada.
# Ficam num lugar só para que o mundo, os agentes e o algoritmo genético usem os mesmos valores.
#
# A ordem de ACOES importa: os sorteios do algoritmo genético e da busca aleatória escolhem
# pela posição na sequência, então mudar a ordem muda os resultados dos experimentos.
"""

# Ações
CIMA = "CIMA"
BAIXO = "BAIXO"
ESQUERDA = "ESQUERDA"
DIREITA = "DIREITA"
AGARRAR = "AGARRAR"
TIRO = "TIRO"

ACOES_DE_MOVIMENTO = (CIMA, BAIXO, ESQUERDA, DIREITA)
ACOES = (*ACOES_DE_MOVIMENTO, AGARRAR, TIRO)

# Quanto cada movimento soma à posição (linha, coluna); a linha 0 fica em cima
DESLOCAMENTOS = {CIMA: (-1, 0), BAIXO: (1, 0), ESQUERDA: (0, -1), DIREITA: (0, 1)}

# Percepções
FEDOR = "FEDOR"  # o Wumpus vivo está numa casa vizinha
BRISA = "BRISA"  # há um poço numa casa vizinha
BRILHO = "BRILHO"  # o ouro está na casa do agente

# Status devolvido por World.step
OK = "OK"
MORTO = "MORTO"
GANHOU = "GANHOU"
FIM_DE_JOGO = (MORTO, GANHOU)
