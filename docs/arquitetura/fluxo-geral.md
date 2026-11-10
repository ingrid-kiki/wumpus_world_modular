# Fluxograma geral

Mostra o caminho do menu do `main.py` até os resultados na pasta do run. O que acontece dentro de cada agente e de cada
benchmark está nos diagramas de sequência e no fluxograma do algoritmo genético.

```mermaid
flowchart TD
    inicio(["python main.py"]) --> menu{"menu_interativo:<br/>qual opção?"}

    menu -- "2, 3 ou 4" --> unica["execucao_unica:<br/>pede tamanho e semente"]
    unica --> executa["agente.run() no terminal"]
    executa --> fimUnico(["Fim: nenhum arquivo é gravado"])

    menu -- "outra" --> invalida(["Fim: opção inválida"])

    menu -- "1" --> args1["Usa os argumentos<br/>de sys.argv"]
    menu -- "5" --> args5["separar_argumentos:<br/>lê a linha digitada"]
    args1 --> validos
    args5 --> validos

    subgraph rodar["rodar_benchmark"]
        validos{"criar_parser:<br/>argumentos válidos?"}
        validos -- "sim" --> carregar["carregar_benchmark:<br/>importa o arquivo escolhido"]
        carregar --> pasta["Cria a pasta do run"]
        pasta --> metadados["salvar_metadados:<br/>metadata.json"]
        metadados --> captura["capturar_saida_terminal:<br/>terminal_output.txt"]
        captura --> falta{"Falta combinar<br/>tamanho e agente?"}

        falta -- "sim" --> logger["Abre o Logger<br/>da combinação"]
        logger --> benchmark["executar_benchmark:<br/>N execuções, semente i em cada uma"]
        benchmark --> parcial["salvar_resultados:<br/>gravação parcial"]
        parcial --> extras{"O resultado tem<br/>dados_extra?"}
        extras -- "sim" --> avancados["gerar_graficos_avancados"]
        extras -- "não" --> falta
        avancados --> falta

        falta -- "não" --> final["salvar_resultados:<br/>gravação final"]
        final --> graficos["gerar_graficos"]
        graficos --> resumo["Mostra o resumo no terminal"]
    end

    validos -- "não" --> erroArgs(["Fim: erro nos argumentos"])
    resumo --> fim(["Fim: resultados na pasta do run"])
```

## Observações

- A pasta do run é `logs/run_AAAAMMDD_HHMMSS/`, ou a indicada em `--saida`.
- `metadata.json` é gravado antes das execuções. Se algo falhar, o registro do que foi pedido continua lá.
- A gravação parcial acontece depois de cada combinação de tamanho e agente, então uma queda perde no máximo a combinação
  em andamento.
- Se `agente.run()` lançar um erro durante o benchmark, `executar_uma` o registra na coluna `erros` e o benchmark continua
  na execução seguinte.
- `carregar_benchmark` usa `benchmark.py` por padrão. A opção `--benchmark` escolhe outro arquivo, como
  `benchmark_fast.py`, `benchmark_custom.py`, `benchmark_graficos.py` ou `benchmark_sideB.py`.
- `reproduzir.py` chama o mesmo `rodar_benchmark` com os argumentos guardados no `metadata.json`, e depois compara os
  resultados com os originais.
- `experimentos/comparar_metodos.py` não passa por este fluxo: tem linha de comando própria e grava em
  `logs/exp31_<fase>_AAAAMMDD_HHMMSS/`.
