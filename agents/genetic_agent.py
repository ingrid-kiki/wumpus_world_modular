# ==============================
# agents/genetic_agent.py
# ==============================
from ga.ga_core import GeneticAlgorithm  # Importa o núcleo do algoritmo genético
from ga.individual import Individual     # Importa a classe de indivíduo

class GeneticAgent:
    def __init__(self, world, population_size=50, gens=100, chrom_length=20):
        # Referência ao ambiente (mundo do Wumpus)
        self.world = world
        # Instancia o algoritmo genético com parâmetros de população, gerações e tamanho do cromossomo
        self.ga = GeneticAlgorithm(population_size, gens, chrom_length)
        # Histórico das ações e percepções do agente
        self.history = []

    def run(self):
        """
        Executa o algoritmo genético para encontrar a melhor sequência de ações.
        """
        # Executa o algoritmo genético e obtém o melhor indivíduo (sequência de ações)
        best = self.ga.run(self.world)
        print("\n🧬 Melhor sequência encontrada pelo algoritmo genético:")
        print(best.chromosome, "\n")
        print("🏆 Pontuação:", best.fitness)
        # Executa a melhor sequência de ações no mundo real
        passo = 1  # Contador de passos
        for action in best.chromosome:
            # Executa a ação no ambiente e obtém percepção e status
            perception, status = self.world.step(action)
            # Salva informações no histórico
            self.history.append({
                "passo": passo,
                "ação": action,
                "perception": perception,
                "status": status
            })
            # Exibe informações do passo atual
            print(f"[Passo {passo}] Ação: {action}")
            print(f"[Passo {passo}] Percepção recebida: {perception}")
            print(f"[Passo {passo}] Status do agente: {status}\n")
            # Se o agente morreu ou venceu, encerra a execução
            if status == 'DEAD' or status == 'WIN':
                break
            passo += 1

