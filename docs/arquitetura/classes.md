# Diagrama de classes

Mostra as 11 classes do programa, com seus atributos, métodos e relações. Ficam de fora as funções soltas de módulos como
`main.py` e `utils/`, a classe interna `DualWriter` de `main.py`, a pasta `pygad/` e os testes.

```mermaid
classDiagram
    class World {
        +size
        +seed
        +rng
        +agent_pos
        +gold_pos
        +wumpus_pos
        +pits
        +is_alive
        +wumpus_alive
        +last_scream
        +won
        +random_pos(exclude)
        +step(action)
        +move_agent(action)
        +interact(action)
        +perceive()
        +is_done()
        +clone()
        +is_adjacent(pos1, pos2)
    }

    class ManualAgent {
        +world
        +run()
    }

    class LogicAgent {
        +world
        +knowledge
        +max_steps
        +perception_history
        +logger
        +run()
        +decide(perception)
    }

    class LogicKnowledgeBase {
        +size
        +perceptions
        +known
        +visits
        +current_pos
        +in_grid(pos)
        +neighbors()
        +update_knowledge(perception)
        +infer_action(perception)
        +update_position(action, new_pos)
    }

    class GeneticAgent {
        +world
        +ga
        +history
        +run()
    }

    class RandomSearchAgent {
        +world
        +avaliacoes
        +chrom_length
        +rng
        +history
        +run()
    }

    class GeneticAlgorithm {
        +rng
        +proximidade
        +pop_size
        +gens
        +chrom_length
        +mutation_rate
        +crossover_rate
        +fitness_history
        +fitness_pop
        +memory_history
        +cpu_history
        +diversidade_history
        +avaliacoes
        +acertos_cache
        -_cache_fitness
        +avaliar(individual, world)
        +run(world, logger)
        +select(population)
        +crossover(p1, p2)
        +mutate(individual)
        +random_action()
    }

    class AGVariante {
        +selecao
        +torneio_k
        +select(population)
    }

    class Individual {
        +chromosome
        +fitness
        +copia()
        +evaluate(world, proximidade)
    }

    class Logger {
        +filepath
        +file
        +write(msg)
        +close()
    }

    class Visualizer {
        +world
        +cell_size
        +screen
        +font
        +clock
        +draw_cell(x, y, color, text)
        +draw_world()
        +run()
    }

    ManualAgent --> World : world
    LogicAgent --> World : world
    GeneticAgent --> World : world
    RandomSearchAgent --> World : world
    Visualizer --> World : world

    LogicAgent *-- LogicKnowledgeBase : knowledge
    GeneticAgent *-- GeneticAlgorithm : ga
    AGVariante --|> GeneticAlgorithm

    GeneticAlgorithm ..> Individual : cria e evolui
    RandomSearchAgent ..> Individual : sorteia e avalia
    GeneticAlgorithm ..> World : recebe em run
    Individual ..> World : simula em uma cópia

    LogicAgent ..> Logger : atributo logger, sempre None
    GeneticAlgorithm ..> Logger : parâmetro logger, nunca informado

    note for Visualizer "Sem uso: nenhum arquivo do programa importa esta classe"
```

## Como ler

| Seta | Significado | Exemplo |
|---|---|---|
| `-->` | A classe guarda uma referência a outra | `LogicAgent` guarda o `World` que recebe |
| `*--` | A classe cria a outra e é dona dela | `GeneticAgent` cria seu `GeneticAlgorithm` |
| `--\|>` | Herança | `AGVariante` herda de `GeneticAlgorithm` |
| `..>` | A classe usa a outra sem guardá-la como parte permanente | `Individual` usa o `World` para avaliar um cromossomo |

## Onde está cada classe

| Classe | Arquivo |
|---|---|
| `World` | `world/world.py` |
| `ManualAgent` | `agents/manual_agent.py` |
| `LogicAgent` | `agents/logic_agent.py` |
| `LogicKnowledgeBase` | `agents/logic_knowledge_base.py` |
| `GeneticAgent` | `agents/genetic_agent.py` |
| `RandomSearchAgent` | `agents/random_search_agent.py` |
| `GeneticAlgorithm` | `ga/ga_core.py` |
| `Individual` | `ga/individual.py` |
| `AGVariante` | `experimentos/comparar_metodos.py` |
| `Logger` | `utils/logger.py` |
| `Visualizer` | `visual/visualizer.py` |

## Observações sobre o código atual

- **Não há classe base de agente.** Os quatro agentes recebem o `World` no construtor e têm um método `run()`, mas isso é
  só uma convenção. O dicionário `AGENTES_DISPONIVEIS` os escolhe pelo nome.
- **Os agentes não usam o `Logger`.** `main.py` e os benchmarks deixam `LogicAgent.logger` como `None`, e
  `GeneticAgent` chama `GeneticAlgorithm.run` sem informar um logger. Quem cria e usa o `Logger` é `rodar_benchmark`, função
  de `main.py`.
- **`GeneticAlgorithm` e `RandomSearchAgent` avaliam com o mesmo fitness**, o método `Individual.evaluate`.
- **`AGVariante` só é usada nos experimentos**, para trocar a seleção por torneio. Ela não entra no menu do `main.py`.
- Classe base, `logger` e `visual/` estão entre os pontos da Etapa 3 do [plano de boas práticas](../plano-boas-praticas.md).
