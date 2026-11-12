# ==============================
# agents/genetic_agent.py
# ==============================
"""
# Este arquivo implementa o GeneticAgent, um agente inteligente para o Wumpus World
# baseado em algoritmos genéticos. O agente utiliza o núcleo do algoritmo genético
# para evoluir sequências de ações, buscando maximizar o desempenho no ambiente.
# Durante a execução, o agente coleta histórico de ações, percepções e status,
# permitindo análise detalhada do comportamento e integração com benchmarks e gráficos.
"""

import numpy as np

from agents.agente import Agente
from ga.ga_core import GeneticAlgorithm  # Importa o núcleo do algoritmo genético
from world.constantes import ACOES


class GeneticAgent(Agente):
    def __init__(
        self,
        world,
        population_size=100,
        gens=500,
        chrom_length=100,
        mutation_rate=0.02,
        crossover_rate=0.8,
        seed=None,
        proximidade=0.0,
    ):
        super().__init__(world)
        # Sem semente explícita, usa a do mundo: mesma semente -> mesmo resultado (#23)
        if seed is None:
            seed = getattr(world, "seed", None)
        # Instancia o algoritmo genético com parâmetros de população, gerações e tamanho do cromossomo
        self.ga = GeneticAlgorithm(
            pop_size=population_size,
            gens=gens,
            chrom_length=chrom_length,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            seed=seed,
            proximidade=proximidade,
        )

    def run(self):
        """
        Executa o algoritmo genético para encontrar a melhor sequência de ações.
        """
        # Executa o algoritmo genético e obtém o melhor indivíduo (sequência de ações)
        ga_results = self.ga.run(self.world)
        best = ga_results["best"]
        print("\n🧬 Melhor sequência encontrada pelo algoritmo genético:")
        print(best.chromosome, "\n")
        print("🏆 Pontuação:", best.fitness)
        # Executa a melhor sequência de ações no mundo real
        self.executar_sequencia(best.chromosome, mostrar=True)

        # Salva dados de fitness médio e final
        mean_fitness_per_gen = [gen_stats["mean"] for gen_stats in ga_results["fitness_history"]]
        final_fitness_dist = ga_results["fitness_pop"][-1] if ga_results["fitness_pop"] else []

        # Mapeia ações para números para que o PCA possa processar os dados
        ACTION_MAP = {action: i for i, action in enumerate(ACOES)}
        final_pop_numeric = [
            [ACTION_MAP.get(gene, -1) for gene in chromosome]  # Usa .get para segurança
            for chromosome in ga_results["final_pop"]
        ]

        dados_extra_formatado = {
            "fitness": mean_fitness_per_gen,
            "fitness_pop": np.array(ga_results["fitness_pop"]),
            "fitness_final": final_fitness_dist,
            "pop_final": final_pop_numeric,
            "memoria": ga_results.get("memoria", []),
            "cpu": ga_results.get("cpu", []),
            "diversidade_vars": ga_results.get("diversidade_vars"),
        }

        # Retorna o histórico de ações e os dados extras
        return self.resultado(dados_extra_formatado)
