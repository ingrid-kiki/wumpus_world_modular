# ==============================
# agents/genetic_agent.py
# ==============================
"""
# Este arquivo implementa o AgenteGenetico, um agente inteligente para o Wumpus World
# baseado em algoritmos genéticos. O agente utiliza o núcleo do algoritmo genético
# para evoluir sequências de ações, buscando maximizar o desempenho no ambiente.
# Durante a execução, o agente coleta histórico de ações, percepções e status,
# permitindo análise detalhada do comportamento e integração com benchmarks e gráficos.
"""

import numpy as np

from agents.agente import Agente
from ga.ga_core import AlgoritmoGenetico  # Importa o núcleo do algoritmo genético
from world.constantes import ACOES


class AgenteGenetico(Agente):
    def __init__(
        self,
        mundo,
        tamanho_populacao=100,
        geracoes=500,
        tamanho_cromossomo=100,
        taxa_mutacao=0.02,
        taxa_cruzamento=0.8,
        semente=None,
        proximidade=0.0,
    ):
        super().__init__(mundo)
        # Sem semente explícita, usa a do mundo: mesma semente -> mesmo resultado (#23)
        if semente is None:
            semente = getattr(mundo, "semente", None)
        # Instancia o algoritmo genético com parâmetros de população, gerações e tamanho do cromossomo
        self.ag = AlgoritmoGenetico(
            tamanho_populacao=tamanho_populacao,
            geracoes=geracoes,
            tamanho_cromossomo=tamanho_cromossomo,
            taxa_mutacao=taxa_mutacao,
            taxa_cruzamento=taxa_cruzamento,
            semente=semente,
            proximidade=proximidade,
        )

    def executar(self):
        """
        Executa o algoritmo genético para encontrar a melhor sequência de ações.
        """
        # Executa o algoritmo genético e obtém o melhor indivíduo (sequência de ações)
        resultado_ag = self.ag.executar(self.mundo)
        melhor = resultado_ag["melhor"]
        print("\n🧬 Melhor sequência encontrada pelo algoritmo genético:")
        print(melhor.cromossomo, "\n")
        print("🏆 Pontuação:", melhor.fitness)
        # Executa a melhor sequência de ações no mundo real
        self.executar_sequencia(melhor.cromossomo, mostrar=True)

        # Salva dados de fitness médio e final
        fitness_medio_por_geracao = [estatisticas["media"] for estatisticas in resultado_ag["historico_fitness"]]
        fitness_final = resultado_ag["fitness_pop"][-1] if resultado_ag["fitness_pop"] else []

        # Mapeia ações para números para que o PCA possa processar os dados
        INDICE_DA_ACAO = {acao: i for i, acao in enumerate(ACOES)}
        populacao_final_numerica = [
            [INDICE_DA_ACAO.get(gene, -1) for gene in cromossomo]  # Usa .get para segurança
            for cromossomo in resultado_ag["populacao_final"]
        ]

        dados_extra_formatado = {
            "fitness": fitness_medio_por_geracao,
            "fitness_pop": np.array(resultado_ag["fitness_pop"]),
            "fitness_final": fitness_final,
            "pop_final": populacao_final_numerica,
            "memoria": resultado_ag.get("memoria", []),
            "cpu": resultado_ag.get("cpu", []),
            "diversidade_vars": resultado_ag.get("diversidade_vars"),
        }

        # Retorna o histórico de ações e os dados extras
        return self.resultado(dados_extra_formatado)
