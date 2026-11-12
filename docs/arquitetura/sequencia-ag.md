# Sequência de uma execução do algoritmo genético

Mostra a troca de mensagens entre as classes quando o agente genético roda uma vez. As regras de seleção, cruzamento, mutação e
fitness estão no [fluxograma do algoritmo genético](fluxo-ag.md).

```mermaid
sequenceDiagram
    participant Q as Quem chama
    participant GA as AgenteGenetico
    participant AG as AlgoritmoGenetico
    participant I as Individuo
    participant M as Mundo

    Q->>GA: executar()
    GA->>AG: executar(mundo)
    AG->>I: cria tamanho_populacao indivíduos aleatórios

    loop geracoes gerações
        loop cada indivíduo da população
            AG->>AG: avaliar(individuo, mundo)
            alt cromossomo já está no cache
                AG->>I: define o fitness guardado
            else cromossomo novo
                AG->>I: avaliar(mundo, proximidade)
                I->>M: clonar()
                M-->>I: cópia do mundo
                loop cada ação, até morrer ou vencer
                    I->>M: agir(acao) na cópia
                    M-->>I: percepção e status
                end
                I-->>AG: fitness atualizado
            end
        end
        AG->>AG: ordena e registra os históricos
        loop até completar a próxima geração
            AG->>AG: selecionar(populacao), duas vezes
            AG->>I: copia() de cada pai escolhido
            alt sorteio menor que taxa_cruzamento
                AG->>AG: cruzar(p1, p2)
            else
                AG->>I: copia() dos dois pais
            end
            AG->>AG: mutar(), em cada filho
        end
    end

    AG->>AG: avaliar() quem ficou sem fitness
    AG-->>GA: melhor indivíduo e históricos

    loop cada ação do melhor, até morrer ou vencer
        GA->>M: agir(acao) no mundo real
        M-->>GA: percepção e status
    end
    GA-->>Q: historico, passos e dados_extra
```

## Observações

- **Quem chama** é `executar_uma`, nos benchmarks, ou `execucao_unica`, nas opções 3 e 4 do menu.
- Toda a evolução acontece em cópias criadas por `Mundo.clonar`. O mundo real só é alterado no final, ao executar o melhor
  indivíduo.
- Os `dados_extra` devolvidos alimentam os gráficos avançados e o arquivo `.npz` do run.
