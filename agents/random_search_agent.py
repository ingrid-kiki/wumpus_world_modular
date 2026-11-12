# ==============================
# agents/random_search_agent.py
# ==============================
"""
# Agente de referência para o agente genético (#31, #16): sorteia sequências de ações, avalia cada
# uma com a mesma função de fitness do AG, simulando cópias do mundo, e executa a melhor.
#
# Serve de patamar mínimo: um método de busca só mostra valor se superar este agente usando o mesmo
# número de avaliações. Por isso o tamanho do cromossomo e o orçamento vêm das mesmas opções do AG.
"""

import random

from agents.agente import Agente
from ga.individual import Individuo


class AgenteAleatorio(Agente):
    def __init__(self, mundo, avaliacoes=50000, tamanho_cromossomo=100, semente=None):
        super().__init__(mundo)
        # Pelo menos uma sequência precisa ser avaliada para haver o que executar
        self.avaliacoes = max(1, avaliacoes)
        self.tamanho_cromossomo = tamanho_cromossomo
        # Sem semente explícita, usa a do mundo, como o agente genético: mesma semente -> mesmo resultado
        self.gerador = random.Random(getattr(mundo, "semente", None) if semente is None else semente)

    def executar(self):
        """Avalia sequências aleatórias e executa a melhor no mundo real."""
        melhor = None
        for _ in range(self.avaliacoes):
            candidato = Individuo(self.tamanho_cromossomo, self.gerador)
            candidato.avaliar(self.mundo)
            if melhor is None or candidato.fitness > melhor.fitness:
                melhor = candidato

        print(f"🎲 Busca aleatória: melhor pontuação {melhor.fitness} em {self.avaliacoes} avaliações")
        self.executar_sequencia(melhor.cromossomo)
        return self.resultado(fitness=melhor.fitness, avaliacoes=self.avaliacoes)
