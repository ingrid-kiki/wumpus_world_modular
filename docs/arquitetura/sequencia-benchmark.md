# Sequência de um benchmark completo

Mostra quem chama quem durante um benchmark com `benchmark.py`, que é o arquivo padrão. O caminho desde o menu está no
[fluxograma geral](fluxo-geral.md), e o que acontece dentro do agente genético está na
[sequência do algoritmo genético](sequencia-ag.md).

```mermaid
sequenceDiagram
    participant R as rodar_benchmark
    participant B as executar_benchmark
    participant E as executar_uma
    participant M as World
    participant A as Agente
    participant S as salvar_resultados
    participant G as utils/graficos

    R->>R: valida argumentos, cria a pasta e grava metadados.json

    loop cada tamanho e cada agente
        R->>R: mostra o início da combinação no terminal
        R->>B: executar_benchmark(agente, tamanho, execucoes, parametros)
        loop execução i, de 0 a N-1
            B->>M: World(size, seed=i)
            B->>A: cria o agente com os parâmetros
            B->>E: executar_uma(agente, mundo, rotulo)
            E->>A: run()
            alt terminou sem erro
                A-->>E: resultado
                E->>M: classificar: lê won e is_alive
                M-->>E: vitória, morte ou sobreviveu
            else lançou uma exceção
                A--xE: erro registrado no stderr
                E->>E: status erro
            end
            E-->>B: status, tempo e resultado
        end
        B-->>R: contagens, tempos e dados_extra
        R->>S: gravação parcial do CSV e do .npz
        opt o resultado tem dados_extra
            R->>G: gerar_graficos_avancados
        end
    end

    R->>S: gravação final
    S-->>R: tabela de resultados e caminho do CSV
    R->>G: gerar_graficos
```

## Observações

- A semente do mundo é o número da execução, então as execuções podem ser repetidas com os mesmos mundos.
- `dados_extra` vem da primeira execução que terminou sem erro. Por isso os gráficos avançados mostram só essa execução
  ([#29](https://github.com/ingrid-kiki/wumpus_world_modular/issues/29)).
- Uma execução com erro entra na coluna `erros` e não conta como vitória, morte ou sobrevivência.
- Com `--paralelo`, as execuções rodam em processos paralelos, com `joblib`, na mesma lógica. Os erros voltam ao processo
  principal e são escritos no `saida_terminal.txt` depois das execuções.
- `tempo_total` é o tempo de relógio da combinação, e `tempo_medio` é a média do tempo de cada execução.
