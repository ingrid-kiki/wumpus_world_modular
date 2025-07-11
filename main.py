# ==============================
# main.py
# ==============================
import argparse  # Módulo para análise de argumentos de linha de comando
from world.world import World  # Importa a classe do ambiente Wumpus
from agents.manual_agent import ManualAgent  # Importa agente manual
from agents.logic_agent import LogicAgent    # Importa agente lógico
from agents.genetic_agent import GeneticAgent  # Importa agente genético
from visual.visualizer import Visualizer  # Importa visualizador gráfico (Pygame)

if __name__ == "__main__":
    # Cria o parser de argumentos para execução via terminal
    parser = argparse.ArgumentParser(description="Executar agente no mundo de Wumpus")
    # Argumento obrigatório: tipo de agente
    parser.add_argument("agente", choices=["manual", "logico", "genetico"], help="Tipo de agente a executar")
    # Argumento opcional: tamanho do mundo
    parser.add_argument("--size", type=int, default=4, help="Tamanho do mundo (padrão: 4x4)")
    # Argumento opcional: semente para aleatoriedade
    parser.add_argument("--seed", type=int, default=None, help="Semente para reprodutibilidade")
    # Argumento opcional: ativa visualização gráfica
    parser.add_argument("--vis", action="store_true", help="Ativar modo visual com Pygame")
    # Analisa os argumentos fornecidos pelo usuário
    args = parser.parse_args()

    # Cria o mundo do Wumpus com os parâmetros fornecidos
    mundo = World(size=args.size, seed=args.seed)

    # Se o modo visual está ativado, executa o visualizador
    if args.vis:
        vis = Visualizer(mundo)
        vis.run()
    else:
        # Seleciona o agente de acordo com o argumento
        if args.agente == "manual":
            agente = ManualAgent(mundo)
        elif args.agente == "logico":
            agente = LogicAgent(mundo)
        elif args.agente == "genetico":
            agente = GeneticAgent(mundo)

        # Exibe qual agente está sendo executado
        print(f"\nExecutando agente: {args.agente.upper()}")
        # Inicia o ciclo de execução do agente escolhido
        agente.run()