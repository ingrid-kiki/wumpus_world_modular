# Sequência de uma execução do algoritmo genético

Mostra a troca de mensagens entre as classes quando o agente genético roda uma vez. As regras de seleção, cruzamento, mutação e
fitness estão no [fluxograma do algoritmo genético](fluxo-ag.md).

```mermaid
sequenceDiagram
    participant Q as Quem chama
    participant GA as GeneticAgent
    participant AG as GeneticAlgorithm
    participant I as Individual
    participant M as World

    Q->>GA: run()
    GA->>AG: run(world)
    AG->>I: cria pop_size indivíduos aleatórios

    loop gens gerações
        loop cada indivíduo da população
            AG->>AG: avaliar(individual, world)
            alt cromossomo já está no cache
                AG->>I: define o fitness guardado
            else cromossomo novo
                AG->>I: evaluate(world, proximidade)
                I->>M: clone()
                M-->>I: cópia do mundo
                loop cada ação, até morrer ou vencer
                    I->>M: step(action) na cópia
                    M-->>I: percepção e status
                end
                I-->>AG: fitness atualizado
            end
        end
        AG->>AG: ordena e registra os históricos
        loop até completar a próxima geração
            AG->>AG: select(population), duas vezes
            AG->>I: copia() de cada pai escolhido
            alt sorteio menor que crossover_rate
                AG->>AG: crossover(p1, p2)
            else
                AG->>I: copia() dos dois pais
            end
            AG->>AG: mutate(), em cada filho
        end
    end

    AG->>AG: avaliar() quem ficou sem fitness
    AG-->>GA: melhor indivíduo e históricos

    loop cada ação do melhor, até morrer ou vencer
        GA->>M: step(action) no mundo real
        M-->>GA: percepção e status
    end
    GA-->>Q: historico, passos e dados_extra
```

## Observações

- **Quem chama** é `executar_uma`, nos benchmarks, ou `execucao_unica`, nas opções 3 e 4 do menu.
- Toda a evolução acontece em cópias criadas por `World.clone`. O mundo real só é alterado no final, ao executar o melhor
  indivíduo.
- Os `dados_extra` devolvidos alimentam os gráficos avançados e o arquivo `.npz` do run.
