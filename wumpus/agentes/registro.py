# ==============================
# wumpus/agentes/registro.py
# ==============================
"""
# Lista única dos agentes do programa, escolhidos pelo nome. O main.py e os benchmarks usam
# este mesmo dicionário: um agente novo entra aqui e passa a valer em todo o programa.
"""

from wumpus.agentes.agente_aleatorio import AgenteAleatorio
from wumpus.agentes.agente_genetico import AgenteGenetico
from wumpus.agentes.agente_logico import AgenteLogico
from wumpus.agentes.agente_manual import AgenteManual
from wumpus.agentes.logico_seguro import AgenteLogicoSeguro

AGENTES_DISPONIVEIS = {
    "manual": AgenteManual,
    "logico": AgenteLogico,
    "logico_seguro": AgenteLogicoSeguro,
    "genetico": AgenteGenetico,
    "aleatorio": AgenteAleatorio,
}

# O agente manual pede ações pelo teclado: não faz sentido em benchmarks (#30, #38)
AGENTES_AUTOMATICOS = [nome for nome in AGENTES_DISPONIVEIS if nome != "manual"]
