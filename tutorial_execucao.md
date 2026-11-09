# 📘 Tutorial de uso do Wumpus World

Este guia mostra **o que o projeto faz hoje e como usar**. Todos os comandos abaixo foram executados e conferidos na
versão 1.6.0. O que ainda não funciona está na [seção 9](#9-o-que-ainda-não-funciona).

Sumário: [instalação](#1-instalação) · [menu](#2-o-menu-do-programa) · [jogar](#3-jogar-com-o-agente-manual) ·
[agentes automáticos](#4-rodar-um-agente-automático-uma-vez) · [benchmark](#5-comparar-agentes-com-o-benchmark) ·
[resultados](#6-onde-ficam-os-resultados) · [reproduzir](#7-reproduzir-uma-execução) ·
[benchmarks avulsos](#8-benchmarks-avulsos) · [limitações](#9-o-que-ainda-não-funciona) · [testes](#10-conferir-a-instalação-com-os-testes)

---

## 1. Instalação

É preciso ter **Python 3.12 ou superior**. No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente. No Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências, que têm versões fixadas para os resultados poderem ser reproduzidos:

```bash
pip install -r requirements.txt
```

---

## 2. O menu do programa

Tudo começa em:

```bash
python main.py
```

```text
=== Wumpus World ===
Escolha o modo de execução:
1 - Benchmark (vários agentes e tamanhos)
2 - Agente Manual (interativo)
3 - Agente Lógico (uma execução)
4 - Agente Genético (uma execução)
5 - Customizado via linha de comando (CLI)
```

| Opção | Para que serve | Gera arquivos? |
|---|---|---|
| 1 ou 5 | Comparar agentes em muitos mundos | Sim, em `logs/` |
| 2 | Você joga, digitando as ações | Não |
| 3 ou 4 | Ver um agente jogar uma partida | Não |

As opções 2, 3 e 4 perguntam o tamanho do mundo e a semente. **A mesma semente gera sempre o mesmo mundo**; deixando
a semente em branco (Enter), o mundo é sorteado.

### As regras em resumo

O mundo é um grid N×N (N a partir de 2), e o agente começa em (0,0), o canto superior esquerdo. As posições são
(linha, coluna).

| Ação | Efeito |
|---|---|
| `CIMA`, `BAIXO`, `ESQUERDA`, `DIREITA` | Anda uma casa. Contra a parede, não acontece nada |
| `AGARRAR` | Pega o ouro, se estiver na casa dele. **Isso vence o jogo** |
| `TIRO` | Mata o Wumpus, se ele estiver em uma casa vizinha. Flechas são ilimitadas e o tiro não tem direção |

| Percepção | Significa |
|---|---|
| `FEDOR` | O Wumpus está em uma casa vizinha (e vivo) |
| `BRISA` | Há um poço em uma casa vizinha |
| `BRILHO` | O ouro está nesta casa |

Entrar na casa de um poço ou do Wumpus vivo mata o agente. As diferenças em relação ao jogo clássico estão na seção
"Regras deste Wumpus World" do [README](README.md).

---

## 3. Jogar com o agente manual

Escolha a opção **2**. Exemplo real, num mundo 4x4 com semente 7 (ouro em (2,1), poços em (1,0) e (2,0)):

```text
Digite o número da opção desejada: 2
Tamanho do mundo (ex: 4): 4
Semente aleatória (opcional, pressione Enter para aleatório): 7

Ação (CIMA, BAIXO, ESQUERDA, DIREITA, AGARRAR, TIRO): pular
❌ Ação inválida: 'PULAR'. Tente novamente.
Ação (...): direita
[Passo 1] Ação: DIREITA | Percepção: [] | Status: OK
Ação (...): baixo
[Passo 2] Ação: BAIXO | Percepção: ['BRISA'] | Status: OK
Ação (...): baixo
[Passo 3] Ação: BAIXO | Percepção: ['BRISA', 'BRILHO'] | Status: OK
Ação (...): agarrar
[Passo 4] Ação: AGARRAR | Percepção: ['BRISA', 'BRILHO'] | Status: GANHOU
```

Maiúsculas e minúsculas tanto faz. O jogo termina quando você vence (`GANHOU`) ou morre (`MORTO`). O mapa não é
mostrado: você decide só pelas percepções.

---

## 4. Rodar um agente automático uma vez

- **Opção 3, agente lógico:** decide passo a passo pelas percepções. Mostra cada percepção e ação, e o histórico no
  final. Ele tem limite de `4 × N²` passos e **morre com frequência**, porque entra em casas desconhecidas mesmo
  sentindo brisa.
- **Opção 4, agente genético:** evolui uma sequência de ações simulando o mundo e depois a executa. Mostra a melhor
  sequência, a pontuação e cada passo. Exemplo real, mundo 6x6 com semente 42: pontuação 106,5, venceu no passo 6.

> O genético e o lógico não jogam nas mesmas condições: o genético planeja simulando o mundo real, e o lógico só usa
> percepções. Veja "Os agentes não jogam nas mesmas condições" no [README](README.md).

---

## 5. Comparar agentes com o benchmark

O benchmark roda os agentes em vários mundos (a execução *i* usa a semente *i*) e grava resultados, gráficos e
metadados. Há duas formas de passar as opções:

**Opção 5 do menu:** o programa pede a linha de opções.

```text
Digite o número da opção desejada: 5
main.py --agentes logico genetico --sizes 4 6 --execucoes 10
```

**Opção 1 do menu:** as opções vão na própria chamada do programa, e depois você digita `1` no menu.

```bash
python main.py --agentes logico --sizes 4 --execucoes 3
```

### Opções

| Opção | Padrão | O que faz |
|---|---|---|
| `--execucoes N` | 32 | Execuções por agente e tamanho |
| `--sizes A B ...` | 4 6 8 | Tamanhos do mundo (mínimo 2) |
| `--agentes A B ...` | logico genetico | `logico`, `genetico`, `aleatorio` (busca aleatória, a referência do genético) |
| `--benchmark ARQUIVO` | benchmark.py | Qual dos 5 arquivos de benchmark usar; `benchmark_fast.py` roda em paralelo |
| `--saida PASTA` | `logs/run_AAAAMMDD_HHMMSS` | Pasta dos resultados |
| `--populacao N` | 100 | Tamanho da população do genético |
| `--geracoes N` | 500 | Número de gerações |
| `--cromossomo N` | 100 | Quantas ações cada indivíduo tem |
| `--mutacao X` | 0.02 | Taxa de mutação (0 a 1) |
| `--cruzamento X` | 0.8 | Taxa de cruzamento (0 a 1) |
| `--proximidade P` | 0 | Bônus no fitness por chegar perto do ouro. Com 0, é o fitness original; nos experimentos da #31, usamos 20 |
| `--avaliacoes N` | população × gerações | Orçamento da busca aleatória |

Exemplo completo, com os parâmetros do genético:

```text
main.py --agentes logico genetico --sizes 4 --execucoes 5 --populacao 50 --geracoes 100 --cromossomo 50 --mutacao 0.05 --cruzamento 0.7 --saida logs/teste
```

No final, o programa mostra o resumo de cada agente e tamanho:

```text
📊 RESULTADOS - GENETICO | Tamanho: 4x4
🏆 Vitórias: 4 (80.0%)
☠️ Mortes: 0 (0.0%)
🤔 Sobreviveu sem vencer: 1 (20.0%)
⏱️ Tempo total: 1.69s | Tempo médio: 0.34s
```

Se alguma execução falhar, ela aparece em uma linha `❌ Erros`, e o benchmark continua com as demais. O detalhe do erro
fica em `terminal_output.txt`.

### Quanto tempo leva

O tempo varia bastante com a máquina e com o que mais estiver rodando. Valores medidos:

| O que | Tempo |
|---|---|
| Agente lógico | Menos de 1 ms por execução |
| Genético com parâmetros padrão (100 × 500 × 100) | De 1 a 6 s por execução |
| Benchmark padrão completo (32 execuções, 3 tamanhos, 2 agentes) | De 4 a 12 min |
| Gráficos avançados | Até 40 s por tamanho de mundo, a maior parte no gráfico de violino |

Para um teste rápido, reduza `--execucoes`, `--geracoes` ou `--populacao`.

---

## 6. Onde ficam os resultados

Cada benchmark cria uma pasta própria:

```text
logs/run_AAAAMMDD_HHMMSS/
├── metadata.json                 versão, commit, opções, parâmetros do genético, bibliotecas
├── resultados_benchmark.csv      uma linha por agente e tamanho
├── terminal_output.txt           tudo o que apareceu no terminal, inclusive erros
├── logico_*.log, genetico_*.log  início e fim de cada benchmark
├── grafico_vitórias.png          comparações entre agentes e tamanhos
├── grafico_mortes.png
├── grafico_sobreviveu.png
├── grafico_tempo_medio.png
├── dados_extra_genetico_4x4.npz  arrays do genético (fitness, diversidade, memória, CPU)
└── advanced_charts_genetico_4x4/ gráficos do genético, um conjunto por tamanho
```

**`resultados_benchmark.csv`** tem as colunas `agente`, `tamanho_mundo`, `vitórias`, `mortes`, `sobreviveu`, `erros`,
`tempo_total` e `tempo_médio`.

**Gráficos avançados** (só para o genético, feitos com os dados da **primeira** execução de cada tamanho):
`evolucao_fitness`, `convergencia_populacao`, `curva_convergencia_std`, `violin_fitness`, `ecdf_fitness_final`,
`heatmap_diversidade`, `area_empilhada_diversidade`, `pca_populacao_final` e `memoria_cpu`.

Para abrir os arrays em Python:

```python
import numpy as np
dados = np.load("logs/run_AAAAMMDD_HHMMSS/dados_extra_genetico_4x4.npz")
print(dados.files)
print(dados["fitness"])
```

**Se a execução for interrompida** (Ctrl+C, queda de energia, erro inesperado), o CSV e os `.npz` ficam com tudo o que
já terminou, e o `terminal_output.txt` guarda o que aconteceu até ali: perde-se no máximo o agente e tamanho em
andamento. Os 4 gráficos de comparação só são gerados no final.

A pasta `logs/` não vai para o git. Para compartilhar resultados, veja o [CONTRIBUTING](CONTRIBUTING.md).

---

## 7. Reproduzir uma execução

Todo benchmark grava o `metadata.json`, e isso permite refazê-lo e conferir se os números se repetem:

```bash
python reproduzir.py logs/run_AAAAMMDD_HHMMSS
```

O script roda de novo, grava em `<pasta>_reproducao` (ou em `--saida PASTA`), avisa se o commit, a versão ou as
bibliotecas forem diferentes e compara vitórias, mortes, sobrevivências e erros:

```text
✅ Resultados idênticos aos originais.
```

| Código de saída | Significado |
|---|---|
| 0 | Resultados iguais |
| 1 | Resultados diferentes |
| 2 | Não dá para comparar (pasta sem `metadata.json` ou sem CSV) |

Tempos, memória e CPU variam a cada rodada e não são comparados. Execuções anteriores à v1.5.0 não têm `metadata.json`.

---

## 8. Benchmarks avulsos

Os arquivos de benchmark também rodam sozinhos, **mas o `main.py` é o caminho recomendado**: só ele grava o
`metadata.json` e aceita os parâmetros do genético. Rodados sozinhos, eles usam os padrões do genético.

| Comando | Opções | O que gera |
|---|---|---|
| `python benchmark.py` | Nenhuma (argumentos são ignorados): 3 execuções em 4x4, lógico e genético | Só resumo na tela |
| `python benchmark_custom.py` | `--execucoes`, `--sizes`, `--agentes`, `--silent` | Só resumo na tela |
| `python benchmark_sideB.py` | Nenhuma: 10 execuções em 4x4, 6x6 e 8x8 | Só resumo na tela |
| `python benchmark_graficos.py` | `--execucoes`, `--sizes`, `--agentes`, `--saida` | CSV e gráficos em `logs/run_.../` |
| `python benchmark_fast.py` | `--execucoes`, `--sizes`, `--agentes` | Roda em paralelo; CSV e gráficos em `logs/run_.../` |

Os cinco dão os mesmos números para os mesmos parâmetros.

---

## 9. O que ainda não funciona

| Item | Situação |
|---|---|
| `python main.py logico --size 4 --vis` | Essa sintaxe não existe ainda: o `main.py` sempre abre o menu. Prevista para a v2.0.0 |
| Janela gráfica (`visual/visualizer.py`) | O código existe, mas não está ligado ao programa |
| Pasta `pygad/` | Não roda: depende do módulo `WumpsimAG`, que não está no projeto ([#15](https://github.com/ingrid-kiki/wumpus_world_modular/issues/15)) |
| Gráficos com todas as execuções | Hoje usam só a primeira ([#29](https://github.com/ingrid-kiki/wumpus_world_modular/issues/29)) |

⚠️ **Sobre interpretar os resultados:** num protótipo, a busca aleatória venceu igual ou mais que o agente genético
com o mesmo número de avaliações. Isso ainda está em investigação
([#31](https://github.com/ingrid-kiki/wumpus_world_modular/issues/31)).

---

## 10. Conferir a instalação com os testes

Para confirmar que está tudo funcionando:

```bash
pip install -r requirements-dev.txt
```

```bash
python -m pytest
```

Todos os testes devem passar.

---

Para saber o que mudou em cada versão, veja o [CHANGELOG](CHANGELOG.md). O histórico das decisões está em
[`docs/`](docs/README.md).
