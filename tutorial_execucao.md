# 📘 Tutorial de Execução - Projeto Wumpus World com Agentes Inteligentes

Este guia mostra como executar o projeto **Wumpus World**, incluindo o uso dos diferentes agentes (manual, lógico, genético), visualização gráfica com Pygame e benchmarks automatizados.

---

## ✅ 1. Pré-requisitos

- Python 3.8 ou superior
- Pip instalado

---

## ✅ 2. Instalar dependências

Abra o terminal no diretório do projeto e execute:

```bash
pip install pygame matplotlib pandas joblib seaborn scikit-learn numpy psutil
```

ou

```bash
pip install -r requirements.txt
```
---

## ✅ 3. Executar o jogo com agentes

### 📌 Sintaxe básica

> ⚠️ **Ainda não implementado.** Hoje o `main.py` só abre o menu interativo (`python main.py`) e ignora
> estes argumentos; o `--vis` também não está ligado ao `Visualizer`. Esta é a sintaxe planejada para a v2.0.0
> (ver [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17)).

```bash
python main.py [AGENTE] [--size N] [--seed VALOR] [--vis]
```

### 🧠 Agentes disponíveis

| Nome       | Descrição                                      |
|------------|-----------------------------------------------|
| `manual`   | Controlado pelo usuário via terminal           |
| `logico`   | Regras simples com mapa interno                |
| `genetico` | IA baseada em algoritmo genético               |

---

### 🎮 Exemplos

```bash
python main.py manual
```

```bash
python main.py logico --size 4 --vis
```

```bash
python main.py genetico --size 6 --seed 42
```

---

## ✅ 4. Como controlar o agente manual

Digite as ações no terminal:

```text
Ação (CIMA, BAIXO, ESQUERDA, DIREITA, AGARRAR, TIRO): up
```

---

## ✅ 5. Visualização com Pygame

Use `--vis` para ativar a interface gráfica:

```bash
python main.py logico --vis
```

---

## ✅ 6. Executar o Benchmark

### Benchmark Padrão
Executa 20 rodadas para cada agente:

```bash
python benchmark.py
```

### Benchmark Customizado
Permite escolher execuções, tamanhos de mundo e agentes:

```bash
python benchmark_custom.py --execucoes 30 --sizes 4 6 8 --agentes logico genetico
```

### Benchmark Alternativo
Executa diferentes tamanhos de mundo (4x4, 6x6, 8x8):

```bash
python benchmark_sideB.py
# executa diferentes tamanhos de mundo (loop sobre 4x4, 6x6, 8x8)
```

### Benchmark com Gráficos
Gera relatórios em CSV e gráficos automáticos (barras, tempo médio, etc):

```bash
python benchmark_graficos.py --execucoes 20 --sizes 4 6 8 --agentes logico genetico
```

### Benchmark Paralelo e Avançado
Executa benchmarks em paralelo, salva resultados e gráficos em subpastas organizadas por execução, e gera gráficos avançados:

```bash
python benchmark_fast.py --execucoes 20 --sizes 4 6 8 --agentes logico genetico
```

---

### Comandos disponíveis:

```bash
python benchmark.py [--execucoes N] [--sizes N1 N2 ...] [--agentes A1 A2 ...] [--silent]
```

### Parâmetros customizáveis:

| Parâmetro     | Descrição                                 | Exemplo                 |
|---------------|---------------------------------------------|--------------------------|
| `--execucoes` | Quantidade de execuções por teste           | `--execucoes 20`         |
| `--sizes`     | Tamanhos do mundo (pode passar vários)      | `--sizes 4 6 8`          |
| `--agentes`   | Lista de agentes a testar                   | `--agentes logico genetico` |
| `--silent`    | Ativa modo silencioso (menos prints)        | `--silent`               |

---
### Exemplos de execução do benchmark

Executar 10 execuções para todos os agentes nos mundos 4x4, 6x6 e 8x8:

```bash
python benchmark.py
```

Executar só o agente lógico 30 vezes no mundo 6x6:

```bash
python benchmark.py --execucoes 30 --sizes 6 --agentes logico
```

Executar em modo silencioso:

```bash
python benchmark.py --silent
```

---

Exemplo de saída:

```
📊 RESULTADOS - Agente: LOGICO | Tamanho: 4x4
🏆 Vitórias: 11 (55.0%)
☠️ Mortes: 5 (25.0%)
🤔 Sobreviveu sem vencer: 4 (20.0%)
⏱️ Tempo total: 2.00 segundos
⏱️ Tempo médio por execução: 0.10 segundos
```

**Resumo dos arquivos de benchmark:**

- `benchmark.py` — Benchmark padrão, executa 20 rodadas para cada agente.
- `benchmark_custom.py` — Permite personalizar execuções, tamanhos de mundo e agentes via argumentos.
- `benchmark_sideB.py` — Benchmark alternativo para cenários e análises diferenciadas.
- `benchmark_graficos.py` — Benchmark com geração automática de gráficos.
- `benchmark_fast.py` — Benchmark paralelo, organizado por pastas, com gráficos avançados.

---

## ✅ 7. Onde ver os logs e resultados?

Os arquivos de log, CSVs e gráficos são salvos automaticamente em subpastas de `/logs/`, organizados por execução e agente:

```
/logs/
└── run_YYYYMMDD_HHMMSS/
    ├── resultados_benchmark.csv
    ├── grafico_vitorias.png
    ├── grafico_mortes.png
    ├── grafico_sobreviveu.png
    ├── grafico_tempo_medio.png
    ├── memoria_cpu.png
    ├── evolucao_fitness.png
    ├── ... (outros gráficos avançados)
    ├── logico_YYYYMMDD_HHMMSS.log
    └── genetico_YYYYMMDD_HHMMSS.log
```

---

## ✅ 8. Estrutura do Projeto

```
.
├── agents/                 # Agentes manuais, lógicos e genéticos
├── ga/                     # Algoritmo genético
├── world/                  # Lógica do mundo do Wumpus
├── visual/                 # Visualização com Pygame
├── utils/                  # Logger e gráficos
├── logs/                   # Gerado automaticamente (organizado por execução)
├── main.py                 # Executa o jogo
├── benchmark.py            # Executa testes comparativos
├── benchmark_custom.py     # Executa testes comparativos customizados
├── benchmark_graficos.py   # Executa testes com geração automática de gráficos
├── benchmark_fast.py       # Executa testes paralelos e gráficos avançados
├── benchmark_sideB.py      # Executa testes comparativos com tamanhos variados de mundos
└── README.md
```

---

## ✅ 9. Gráficos Avançados

Quando os dados são coletados (especialmente pelo agente genético), o projeto gera automaticamente:

- **Memória + CPU + Distribuição dos Recursos**
- **Evolução do Fitness (convergência)**
- **Comportamento de Convergência da População (mínimo, médio e máximo)**
- **Média das Curvas de Convergência com Desvio Padrão**
- **Plot do Violino**
- **Função de Distribuição Acumulada (ECDF)**
- **Mapa de Calor da Diversidade por Variável**
- **Gráfico de Área Empilhada da Diversidade por Variável**
- **PCA para Visualizar Agrupamentos Genéticos**

Todos os gráficos são salvos automaticamente na subpasta de cada execução.

---

## 💡 Dica extra

Quer repetir o mesmo cenário para testes? Use:

```bash
python main.py logico --seed 123
```

---

## 👩‍💻 Autoria

Este projeto é mantido por **Alfa Marine** e **Ingrid Mendes**, com foco em IA, jogos e ensino computacional.