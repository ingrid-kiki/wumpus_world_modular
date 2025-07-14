# ga_pygad.py
import pygad
import numpy as np
import WumpsimAG

# Dicionário para passar o contexto da simulação para a função de fitness,
# já que a assinatura da função no PyGAD é fixa.
_context = {
    "wumpus_world": None,
    "seed": None,
    "size_cromo": None
}

def _set_context(wumpus_world, seed, size_cromo):
    """Define o contexto para a avaliação de fitness de cada geração."""
    _context["wumpus_world"] = wumpus_world
    _context["seed"] = seed
    _context["size_cromo"] = size_cromo

def _fitness_function(ga_instance, solution, solution_idx):
    """
    Função de Fitness para o PyGAD.
    Executa uma simulação do Mundo de Wumpus para um 'indivíduo' (sequência de ações)
    e retorna sua pontuação. O PyGAD trabalha para maximizar este valor.
    """
    # O WumpsimAG.run retorna múltiplas métricas. O 'total_score' é a pontuação
    # normalizada pelo número de movimentos, um bom candidato para fitness.
    _avg_score, total_score, _h, _d, _w, _a = WumpsimAG.run(
        AG_moves=solution,
        print_world=False,
        size_cromo=_context["size_cromo"],
        seed=_context["seed"],
        world_generated=_context["wumpus_world"]
    )
    return total_score

def _get_state_for_solution(solution):
    """
    Re-executa a simulação para um indivíduo específico para obter seu estado final
    detalhado (ouro, wumpus morto, vitória, etc.).
    """
    _avg_score, _total_score, has_gold, death_wumpus, win, alive = WumpsimAG.run(
        AG_moves=solution,
        print_world=False,
        size_cromo=_context["size_cromo"],
        seed=_context["seed"],
        world_generated=_context["wumpus_world"]
    )
    return has_gold, death_wumpus, win, alive

def solve_with_pygad(params):
    """
    Função principal que configura e executa o Algoritmo Genético com PyGAD.
    Esta função substitui o laço de gerações manual do script original.

    Args:
        params (dict): Dicionário contendo todos os parâmetros do AG e do ambiente.

    Returns:
        tuple: Contendo as listas best_outputs, best_cromo, e best_current_state.
    """
    # Define o contexto para a execução atual
    _set_context(params['wumpus_world'], params['seed'], params['size_chromo'])

    # Listas para armazenar o histórico da evolução, similar ao script original
    best_outputs = []
    best_cromo_per_gen = []
    best_states_per_gen = []

    def on_generation(ga_instance):
        """
        Callback executado ao final de cada geração para coletar dados.
        """
        solution, fitness, _ = ga_instance.best_solution()
        
        # O script original minimizava o fitness (que era -score).
        # PyGAD maximiza o score. Armazenamos o fitness real (maior é melhor).
        best_outputs.append(fitness)
        best_cromo_per_gen.append(solution)
        best_states_per_gen.append(_get_state_for_solution(solution))

    # Calcula o número de indivíduos para o elitismo
    keep_elitism = int(params['elit_ratio'] * params['size_pop'])

    # O limite superior do gene_space no PyGAD é exclusivo
    gene_space = {'low': params['min_gene'], 'high': params['max_gene'] + 1}

    # Instancia o objeto PyGAD com os parâmetros
    ga_instance = pygad.GA(
        num_generations=params['num_generations'],
        sol_per_pop=params['size_pop'],
        num_genes=params['size_chromo'],
        num_parents_mating=params['num_parents_mating'],
        fitness_func=_fitness_function,
        
        parent_selection_type="tournament",
        K_tournament=params['tournament_number'],
        
        keep_elitism=keep_elitism,
        
        crossover_type="single_point",
        crossover_probability=params['crossover_probability'],
        
        mutation_type="random",
        mutation_probability=params['mutation_probability'],
        mutation_by_replacement=True,
        
        gene_space=gene_space,
        
        on_generation=on_generation,
        
        suppress_warnings=True,
        allow_duplicate_genes=True # Ações podem se repetir no cromossomo
    )

    # Inicia o processo de evolução
    ga_instance.run()

    # O script original espera fitnesses a serem minimizados. Para manter a compatibilidade
    # de análise dos resultados, podemos retornar o negativo do score.
    # No entanto, é mais correto trabalhar com o score real onde maior é melhor.
    # A adaptação será feita no script principal.
    return best_outputs, best_cromo_per_gen, best_states_per_gen
