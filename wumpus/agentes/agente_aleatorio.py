# ==============================
# wumpus/agentes/agente_aleatorio.py
# ==============================
"""
# Agente de referência para o agente genético (#31, #16): sorteia sequências de ações, avalia cada
# uma com a mesma função de fitness do AG, simulando cópias do mundo, e executa a melhor.
#
# Serve de patamar mínimo: um método de busca só mostra valor se superar este agente usando o mesmo
# número de avaliações. Por isso o tamanho do cromossomo e o orçamento vêm das mesmas opções do AG.
"""

import random

from wumpus.ag.individuo import Individuo, fitness_de
from wumpus.agentes.agente import Agente, Resultado
from wumpus.mundo.mundo import Mundo


class AgenteAleatorio(Agente):
    def __init__(
        self, mundo: Mundo, avaliacoes: int = 50000, tamanho_cromossomo: int = 100, semente: int | None = None
    ) -> None:
        super().__init__(mundo)
        # Pelo menos uma sequência precisa ser avaliada para haver o que executar
        self.avaliacoes = max(1, avaliacoes)
        self.tamanho_cromossomo = tamanho_cromossomo
        # Sem semente explícita, usa a do mundo, como o agente genético: mesma semente -> mesmo resultado
        self.gerador = random.Random(getattr(mundo, "semente", None) if semente is None else semente)

    def executar(self) -> Resultado:
        """Avalia sequências aleatórias e executa a melhor no mundo real."""
        melhor: Individuo | None = None
        for _ in range(self.avaliacoes):
            candidato = Individuo(self.tamanho_cromossomo, self.gerador)
            candidato.avaliar(self.mundo)
            if melhor is None or fitness_de(candidato) > fitness_de(melhor):
                melhor = candidato
        assert melhor is not None  # avaliacoes é pelo menos 1

        print(f"🎲 Busca aleatória: melhor pontuação {melhor.fitness} em {self.avaliacoes} avaliações")
        self.executar_sequencia(melhor.cromossomo)
        return self.resultado(fitness=melhor.fitness, avaliacoes=self.avaliacoes)
