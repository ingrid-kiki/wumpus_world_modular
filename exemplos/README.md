# Exemplos de execução

Varredura de parâmetros do **agente genético** feita em 16–17/07/2025 com a versão **v1.3.0** do código.

> ⚠️ **Estes resultados foram gerados antes das correções da Fase 3** (fitness desatualizado após mutação,
> ouro pontuado várias vezes, poços sobrepostos, RNG global). Use-os como registro histórico,
> não como comparação com versões futuras.

## Onde estão os dados completos

Os 34 runs completos (CSV, `terminal_output.txt` e todos os gráficos), junto com a antiga pasta `logs/`,
estão no pacote **`wumpus_dados_v1.3.0.zip`**, publicado no GitHub Release
[`v1.3.0-dados`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.3.0-dados).
Dentro do zip, a estrutura original foi mantida: `exemplos/exemplo_N/run_AAAAMMDD_HHMMSS/`.

## Como cada exemplo foi rodado

Todos usaram a opção 5 do menu do `main.py`, com 50 execuções por tamanho de mundo:

```
main.py 5 --agentes genetico --sizes <tamanhos> --execucoes 50
```

Os parâmetros do AG (população, gerações, cromossomo, taxas) eram alterados **direto no código**
(`agents/genetic_agent.py`) entre um exemplo e outro.

## Resumo

Vitórias em 50 execuções e tempo médio por execução, na ordem dos tamanhos de mundo.

| Ex. | População | Gerações | Cromossomo | Mutação | Cruzamento | Tamanhos | Vitórias | Tempo médio (s) | Run |
|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | 50 | 100 | 20 | 0,02 | 0,3 | 4 6 8 | 41 / 32 / 18 | 0.40 / 0.41 / 0.40 | `run_20250716_210318` |
| 2 | 50 | 100 | 20 | 0,02 | 0,8 | 4 6 8 | 41 / 34 / 18 | 0.39 / 0.38 / 0.41 | `run_20250716_210619` |
| 3 | 50 | 100 | 20 | 0,1 | 0,3 | 4 6 8 | 44 / 39 / 26 | 0.36 / 0.37 / 0.41 | `run_20250716_210938` |
| 4 | 50 | 100 | 20 | 0,1 | 0,8 | 4 6 8 | 41 / 37 / 28 | 0.37 / 0.37 / 0.42 | `run_20250716_211127` |
| 5 | 50 | 100 | 100 | 0,02 | 0,3 | 4 6 8 | 45 / 49 / 43 | 0.93 / 1.08 / 1.10 | `run_20250716_211615` |
| 6 | 50 | 100 | 100 | 0,02 | 0,8 | 4 6 8 | 45 / 45 / 40 | 0.92 / 1.13 / 1.20 | `run_20250716_212157` |
| 7 | 50 | 100 | 100 | 0,1 | 0,3 | 4 6 8 | 49 / 48 / 46 | 0.81 / 1.02 / 1.01 | `run_20250716_212753` |
| 8 | 50 | 100 | 100 | 0,1 | 0,8 | 4 6 8 | 49 / 48 / 47 | 0.81 / 0.96 / 1.06 | `run_20250716_213325` |
| 9 | 50 | 500 | 20 | 0,02 | 0,3 | 4 6 8 | 42 / 34 / 21 | 1.67 / 1.91 / 2.00 | `run_20250716_213828` |
| 10 | 50 | 500 | 20 | 0,02 | 0,8 | 4 6 8 | 41 / 34 / 24 | 1.67 / 1.92 / 2.05 | `run_20250716_214718` |
| 11 | 50 | 500 | 20 | 0,1 | 0,3 | 4 6 8 | 45 / 44 / 27 | 1.67 / 1.91 / 1.98 | `run_20250716_215806` |
| 12 | 50 | 500 | 20 | 0,1 | 0,8 | 4 6 8 | 44 / 39 / 29 | 1.68 / 1.95 / 1.79 | `run_20250716_220651` |
| 13 | 50 | 500 | 100 | 0,02 | 0,3 | 4 6 8 | 49 / 49 / 43 | 5.33 / 5.88 / 6.23 | `run_20250716_221541` |
| 14 | 50 | 500 | 100 | 0,02 | 0,8 | 4 6 8 | 48 / 46 / 42 | 4.72 / 5.69 / 6.19 | `run_20250717_105203` |
| 15 | 50 | 500 | 100 | 0,1 | 0,3 | 4 6 8 | 49 / 48 / 46 | 4.62 / 5.51 / 6.08 | `run_20250717_083104` |
| 16 | 50 | 500 | 100 | 0,1 | 0,8 | 4 6 8 | 49 / 48 / 49 | 4.81 / 4.95 / 5.63 | `run_20250717_085751` |
| 17 | 100 | 100 | 20 | 0,02 | 0,3 | 4 6 8 | 43 / 35 / 24 | 0.74 / 0.79 / 0.86 | `run_20250717_091545` |
| 18 | 100 | 100 | 20 | 0,02 | 0,8 | 4 6 8 | 44 / 37 / 23 | 0.76 / 0.78 / 0.90 | `run_20250717_091830` |
| 19 | 100 | 100 | 20 | 0,1 | 0,3 | 4 6 8 | 44 / 41 / 27 | 0.76 / 0.82 / 0.86 | `run_20250717_092229` |
| 20 | 100 | 100 | 20 | 0,1 | 0,8 | 4 6 8 | 44 / 43 / 35 | 0.73 / 0.80 / 0.84 | `run_20250717_092744` |
| 21 | 100 | 100 | 100 | 0,02 | 0,3 | 4 6 8 | 47 / 48 / 47 | 2.15 / 2.40 / 2.59 | `run_20250717_093139` |
| 22 | 100 | 100 | 100 | 0,02 | 0,8 | 4 6 8 | 48 / 49 / 49 | 2.30 / 2.57 / 2.59 | `run_20250717_094053` |
| 23 | 100 | 100 | 100 | 0,1 | 0,3 | 4 6 8 | 49 / 50 / 50 | 1.97 / 2.21 / 2.25 | `run_20250717_094933` |
| 24 | 100 | 100 | 100 | 0,1 | 0,8 | 4 6 8 | 49 / 49 / 48 | 2.01 / 2.24 / 2.49 | `run_20250717_095636` |
| 25 | 100 | 500 | 20 | 0,02 | 0,3 | 4 6 8 | 43 / 37 / 24 | 3.85 / 4.19 / 4.72 | `run_20250717_100342` |
| 26 | 100 | 500 | 20 | 0,02 | 0,8 | 4 6 8 | 44 / 40 / 27 | 3.83 / 3.97 / 3.88 | `run_20250717_102103` |
| 27 | 100 | 500 | 20 | 0,1 | 0,3 | 4 6 8 | 45 / 44 / 34 | 3.41 / 4.09 / 4.21 | `run_20250717_104320` |
| 28 | 100 | 500 | 20 | 0,1 | 0,8 | 4 6 8 | 44 / 44 / 38 | 3.18 / 3.51 / 3.74 | `run_20250717_105638` |
| 29 | 100 | 500 | 100 | 0,02 | 0,8 | 4 6 8 | 49 / 48 / 47 | 10.73 / 10.69 / 11.92 | `run_20250717_113448` |
| 30 | 100 | 500 | 100 | 0,02 | 0,8 | 4 6 8 | 48 / 49 / 50 | 10.25 / 11.07 / 12.69 | `run_20250717_120727` |
| 31 | 100 | 500 | 100 | 0,1 | 0,3 | 4 6 8 | 49 / 50 / 50 | 9.43 / 10.53 / 10.68 | `run_20250717_125527` |
| 32 | 100 | 500 | 100 | 0,1 | 0,8 | 4 6 8 | 49 / 49 / 49 | 8.71 / 10.39 / 11.33 | `run_20250717_132451` |
| 33 | 100 | 500 | 100 | 0,02 | 0,8 | 4 6 8 10 12 14 | 48 / 49 / 50 / 46 / 42 / 38 | 10.49 / 11.98 / 12.06 / 12.52 / 13.85 / 14.62 | `run_20250717_195525` |
| 34 | 100 | 500 | 100 | 0,02 | 0,8 | 10 12 14 | 46 / 42 / 38 | 12.65 / 12.30 / 13.53 | `run_20250717_210840` |

**Observação:** os exemplos 29 e 30 têm os mesmos parâmetros anotados (cruzamento 0,8). Pela sequência da varredura,
o exemplo 29 provavelmente usou cruzamento **0,3**; vale conferir no `terminal_output.txt` do pacote de dados.

## Galeria

A pasta [`galeria/`](galeria/) guarda uma amostra dos gráficos do **exemplo 33**
(população 100, 500 gerações, cromossomo 100, mutação 0,02, cruzamento 0,8):

- `grafico_*.png`: vitórias, mortes, sobrevivência e tempo médio para os mundos 4x4 a 14x14.
- `8x8_*.png`: gráficos avançados do AG no mundo 8x8 (convergência, diversidade, ECDF, PCA, memória/CPU, violino).
