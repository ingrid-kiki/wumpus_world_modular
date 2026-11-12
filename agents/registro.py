# ==============================
# agents/registro.py
# ==============================
"""
# Lista única dos agentes do programa, escolhidos pelo nome. O main.py e os benchmarks usam
# este mesmo dicionário: um agente novo entra aqui e passa a valer em todo o programa.
"""

from agents.genetic_agent import GeneticAgent
from agents.logic_agent import LogicAgent
from agents.logico_seguro import AgenteLogicoSeguro
from agents.manual_agent import ManualAgent
from agents.random_search_agent import RandomSearchAgent

AGENTES_DISPONIVEIS = {
    "manual": ManualAgent,
    "logico": LogicAgent,
    "logico_seguro": AgenteLogicoSeguro,
    "genetico": GeneticAgent,
    "aleatorio": RandomSearchAgent,
}

# O agente manual pede ações pelo teclado: não faz sentido em benchmarks (#30, #38)
AGENTES_AUTOMATICOS = [nome for nome in AGENTES_DISPONIVEIS if nome != "manual"]
