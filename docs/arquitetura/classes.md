# Diagrama de classes

Mostra as 13 classes do programa, com seus atributos, métodos e relações. Ficam de fora as funções soltas de módulos como
`main.py` e `utils/`, a classe interna `SaidaDupla` de `main.py` e os testes.

```mermaid
classDiagram
    class Mundo {
        +tamanho
        +semente
        +gerador
        +posicao_agente
        +posicao_ouro
        +posicao_wumpus
        +pocos
        +agente_vivo
        +wumpus_vivo
        +grito
        +ganhou
        +posicao_aleatoria(excluir)
        +agir(acao)
        +mover_agente(acao)
        +interagir(acao)
        +perceber()
        +terminou()
        +clonar()
        +adjacentes(pos_a, pos_b)
    }

    class Agente {
        <<abstrata>>
        +mundo
        +historico
        +executar()
        +registrar_passo(acao, percepcao, status)
        +executar_sequencia(acoes, mostrar)
        +resultado(dados_extra)
    }

    class AgenteManual {
        +executar()
    }

    class AgenteLogico {
        +conhecimento
        +max_passos
        +executar()
        +decidir_acao(percepcao)
    }

    class BaseConhecimento {
        +tamanho
        +percepcoes
        +conhecidas
        +visitas
        +posicao_atual
        +dentro_do_mundo(pos)
        +vizinhas_validas()
        +atualizar_conhecimento(percepcao)
        +inferir_acao(percepcao)
        +atualizar_posicao(acao, nova_posicao)
    }

    class AgenteLogicoSeguro {
        +conhecimento
    }

    class BaseConhecimentoSegura {
        +vizinhas_de(pos)
        +casas_seguras()
        +fronteira()
        +suspeita(casa)
        +poco_certo(casa, seguras)
        +primeiro_passo_ate(alvos)
        +arriscar(fronteira, seguras)
        +permanecer()
        +inferir_acao(percepcao)
    }

    class AgenteGenetico {
        +ag
        +executar()
    }

    class AgenteAleatorio {
        +avaliacoes
        +tamanho_cromossomo
        +gerador
        +executar()
    }

    class AlgoritmoGenetico {
        +gerador
        +proximidade
        +tamanho_populacao
        +geracoes
        +tamanho_cromossomo
        +taxa_mutacao
        +taxa_cruzamento
        +historico_fitness
        +fitness_populacao
        +historico_memoria
        +historico_cpu
        +historico_diversidade
        +avaliacoes
        +acertos_cache
        -_cache_fitness
        +avaliar(individuo, mundo)
        +executar(mundo)
        +selecionar(populacao)
        +cruzar(p1, p2)
        +mutar(individuo)
        +acao_aleatoria()
        -_registrar_recursos(processo)
        -_registrar_geracao(populacao)
        -_proxima_geracao(populacao)
        -_resultado(melhor_individuo, populacao)
    }

    class AGVariante {
        +selecao
        +torneio_k
        +selecionar(populacao)
    }

    class Individuo {
        +cromossomo
        +fitness
        +copia()
        +avaliar(mundo, proximidade)
    }

    class Visualizador {
        +mundo
        +tamanho_casa
        +tela
        +fonte
        +fonte_pequena
        +relogio
        +desenhar_casa(x, y, cor, texto)
        +desenhar_mundo(passo)
        +reproduzir(historico, passos_por_segundo, esperar_fechar)
        -_percepcao_na_casa(pos)
        -_desenhar_percepcoes()
        -_desenhar_elementos()
        -_desenhar_avisos(passo)
        -_fechou()
        -_esperar_fechar()
    }

    Agente --> Mundo : mundo
    AgenteManual --|> Agente
    AgenteLogico --|> Agente
    AgenteGenetico --|> Agente
    AgenteAleatorio --|> Agente
    Visualizador --> Mundo : mundo

    AgenteLogico *-- BaseConhecimento : conhecimento
    AgenteGenetico *-- AlgoritmoGenetico : ag
    AGVariante --|> AlgoritmoGenetico
    AgenteLogicoSeguro --|> AgenteLogico
    BaseConhecimentoSegura --|> BaseConhecimento
    AgenteLogicoSeguro *-- BaseConhecimentoSegura : conhecimento

    AlgoritmoGenetico ..> Individuo : cria e evolui
    AgenteAleatorio ..> Individuo : sorteia e avalia
    AlgoritmoGenetico ..> Mundo : recebe em executar
    Individuo ..> Mundo : simula em uma cópia


```

## Como ler

| Seta | Significado | Exemplo |
|---|---|---|
| `-->` | A classe guarda uma referência a outra | `AgenteLogico` guarda o `Mundo` que recebe |
| `*--` | A classe cria a outra e é dona dela | `AgenteGenetico` cria seu `AlgoritmoGenetico` |
| `--\|>` | Herança | `AGVariante` herda de `AlgoritmoGenetico` |
| `..>` | A classe usa a outra sem guardá-la como parte permanente | `Individuo` usa o `Mundo` para avaliar um cromossomo |

## Onde está cada classe

| Classe | Arquivo |
|---|---|
| `Mundo` | `world/world.py` |
| `AgenteManual` | `agents/manual_agent.py` |
| `AgenteLogico` | `agents/logic_agent.py` |
| `BaseConhecimento` | `agents/logic_knowledge_base.py` |
| `Agente` | `agents/agente.py` |
| `AgenteLogicoSeguro` | `agents/logico_seguro.py` |
| `BaseConhecimentoSegura` | `agents/logico_seguro.py` |
| `AgenteGenetico` | `agents/genetic_agent.py` |
| `AgenteAleatorio` | `agents/random_search_agent.py` |
| `AlgoritmoGenetico` | `ga/ga_core.py` |
| `Individuo` | `ga/individual.py` |
| `AGVariante` | `experimentos/comparar_metodos.py` |
| `Visualizador` | `visual/visualizer.py` |

## Observações sobre o código atual

- **Todos os agentes herdam de `Agente`**, a classe base abstrata. Ela guarda o `Mundo` e o `historico`, e `executar()` devolve o
  resultado no formato único: `historico`, `passos` e `dados_extra`. A lista única `AGENTES_DISPONIVEIS`, em
  `agents/registro.py`, escolhe os agentes pelo nome em todo o programa.
- **`AgenteLogicoSeguro` herda de `AgenteLogico`** e só troca a base de conhecimento: o laço de percepção e ação é o mesmo,
  e a decisão passa a evitar poços ([investigação de 11/11/2026](../investigacao-agente-logico-2026-11.md)).
- **`AlgoritmoGenetico` e `AgenteAleatorio` avaliam com o mesmo fitness**, o método `Individuo.avaliar`.
- **`AGVariante` só é usada nos experimentos**, para trocar a seleção por torneio. Ela não entra no menu do `main.py`.
- **`Visualizador` reproduz uma partida já jogada.** O `main.py` a oferece no fim das execuções únicas, com uma cópia do mundo
  no estado inicial e o histórico do agente.
