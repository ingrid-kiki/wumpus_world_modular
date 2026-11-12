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
from ga.individual import Individual


class RandomSearchAgent(Agente):
    def __init__(self, world, avaliacoes=50000, chrom_length=100, seed=None):
        super().__init__(world)
        # Pelo menos uma sequência precisa ser avaliada para haver o que executar
        self.avaliacoes = max(1, avaliacoes)
        self.chrom_length = chrom_length
        # Sem semente explícita, usa a do mundo, como o agente genético: mesma semente -> mesmo resultado
        self.rng = random.Random(getattr(world, "seed", None) if seed is None else seed)

    def run(self):
        """Avalia sequências aleatórias e executa a melhor no mundo real."""
        melhor = None
        for _ in range(self.avaliacoes):
            candidato = Individual(self.chrom_length, self.rng)
            candidato.evaluate(self.world)
            if melhor is None or candidato.fitness > melhor.fitness:
                melhor = candidato

        print(f"🎲 Busca aleatória: melhor pontuação {melhor.fitness} em {self.avaliacoes} avaliações")
        self.executar_sequencia(melhor.chromosome)
        return self.resultado(fitness=melhor.fitness, avaliacoes=self.avaliacoes)
