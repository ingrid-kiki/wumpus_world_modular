# ==============================
# agents/registro.py
# ==============================
"""
# Lista única dos agentes do programa, escolhidos pelo nome. O main.py e os benchmarks usam
# este mesmo dicionário: um agente novo entra aqui e passa a valer em todo o programa.
"""

from agents.genetic_agent import AgenteGenetico
from agents.logic_agent import AgenteLogico
from agents.logico_seguro import AgenteLogicoSeguro
from agents.manual_agent import AgenteManual
from agents.random_search_agent import AgenteAleatorio

AGENTES_DISPONIVEIS = {
    "manual": AgenteManual,
    "logico": AgenteLogico,
    "logico_seguro": AgenteLogicoSeguro,
    "genetico": AgenteGenetico,
    "aleatorio": AgenteAleatorio,
}

# O agente manual pede ações pelo teclado: não faz sentido em benchmarks (#30, #38)
AGENTES_AUTOMATICOS = [nome for nome in AGENTES_DISPONIVEIS if nome != "manual"]
