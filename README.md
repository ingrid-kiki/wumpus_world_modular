# 🧠 Wumpus World com Agentes Inteligentes

Este projeto simula o clássico **Wumpus World** com suporte a **diferentes tipos de agentes inteligentes** (manual, lógico e genético), e inclui uma interface visual interativa com **Pygame**.

> 💡 Ideal para fins didáticos, estudo de IA simbólica, algoritmos genéticos e jogos baseados em agentes.

---

## 🎯 Objetivos

- Explorar diferentes estratégias de tomada de decisão em ambientes incertos.
- Comparar abordagens **manuais**, **baseadas em lógica simbólica** e **algoritmos genéticos**.
- Visualizar o ambiente e as ações dos agentes em tempo real.
- Realizar benchmarks automatizados, com coleta de métricas, logs e geração de gráficos avançados.

---

## 🧩 Estrutura do Projeto

```
.
├── agents/               # Agentes implementados
│   ├── genetic_agent.py
│   ├── logic_agent.py
│   ├── logic_knowledge_base.py
│   └── manual_agent.py
│
├── ga/                   # Núcleo do algoritmo genético
│   ├── ga_core.py
│   └── individual.py
│
├── visual/               # Visualização gráfica com Pygame
│   └── visualizer.py
│
├── world/                # Ambiente do mundo de Wumpus
│   └── world.py
│
├── utils/                # Utilitários do projeto
│   ├── graficos.py       # Geração de gráficos básicos e avançados
│   └── logger.py         # Logger para logs organizados por execução
│
├── logs/                 # Saída dos logs e resultados de benchmarks
│   └── run_YYYYMMDD_HHMMSS/   # Subpastas por execução, com CSVs, PNGs e logs
│      └── advanced_charts_agent_size/   # Resultados dos gráficos avançados
│
├── benchmark.py               # Benchmark padrão (4x4)
├── benchmark_custom.py        # Benchmark customizável via argumentos
├── benchmark_fast.py          # Benchmark paralelo, organizado por pastas
├── benchmark_graficos.py      # Benchmark com geração automática de gráficos
├── benchmark_sideB.py         # Benchmark alternativo para comparação
├── main.py                    # Script principal para execução
└── README.md                  # Este arquivo
```

---

## 🧪 Requisitos

- Python 3.8 ou superior
- Pygame
- matplotlib
- pandas
- joblib
- seaborn
- scikit-learn
- numpy
- psutil

### Instalação de dependências

```bash
pip install pygame matplotlib pandas joblib seaborn scikit-learn numpy psutil
```

ou

```bash
pip install requirements.txt
```
---

## 🚀 Como Executar

Você pode escolher entre 3 agentes: `manual`, `logico`, `genetico`.

### 🔧 Sintaxe

```bash
python main.py [agente] [--size TAMANHO] [--seed SEMENTE] [--vis]
```

### 📌 Exemplos

**Executar agente lógico em mundo 4x4 com visualização:**

```bash
python main.py logico --size 4 --vis
```

**Executar agente genético em mundo 6x6 com semente aleatória:**

```bash
python main.py genetico --size 6 --seed 42
```

**Executar agente manual (via terminal):**

```bash
python main.py manual
```

---

## 🧠 Tipos de Agentes

| Tipo      | Descrição |
|-----------|-----------|
| `manual`  | Agente controlado pelo teclado do usuário. |
| `logico`  | Agente baseado em lógica simbólica simples (regras IF/ELSE). |
| `genetico`| Agente baseado em algoritmo genético com avaliação de desempenho. |

---

## 🖼️ Interface Visual

Ao executar com `--vis`, o ambiente é mostrado em uma janela gráfica com:

- 🟥 Wumpus  
- 🕳️ Poços  
- 🟡 Ouro  
- 🟢 Agente  
- 📣 Grito (se o Wumpus morrer)  
- ☠️ Morte do agente  
- 🏆 Vitória (pegou o ouro)

---

## 📊 Benchmarks e Gráficos

Compare o desempenho dos agentes de forma automatizada, com resultados organizados em subpastas de `/logs` e geração de gráficos básicos e avançados.

### Benchmark Padrão
Executa 20 rodadas para cada agente:
```bash
python benchmark.py
```

### Benchmark Customizado
Permite definir número de execuções, tamanhos de mundo e agentes:
```bash
python benchmark_custom.py --execucoes 30 --sizes 4 6 8 --agentes logico genetico
```

### Benchmark Alternativo
Executa benchmarks em diferentes tamanhos de mundo (4x4, 6x6, 8x8):
```bash
python benchmark_sideB.py 
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

Os gráficos e resultados serão salvos como arquivos PNG e CSV em subpastas dentro de `/logs/run_YYYYMMDD_HHMMSS/`.

---

## 📈 Gráficos Avançados

Além dos gráficos básicos, o projeto gera automaticamente (quando os dados são coletados):

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

## 📁 Logs

Os arquivos de log são salvos automaticamente em subpastas de `/logs/`, organizados por execução e agente:

```
/logs/
└── run_YYYYMMDD_HHMMSS/
    ├── resultados_benchmark.csv
    ├── grafico_vitorias.png
    ├── grafico_mortes.png
    ├── grafico_sobreviveu.png
    ├── grafico_tempo_medio.png
    ├── logico_YYYYMMDD_HHMMSS.log
    ├── genetico_YYYYMMDD_HHMMSS.log
    └── advanced_charts_agent_size/   # Resultados dos gráficos avançados
        ├── convergencia_populacao.png
        ├── evolucao_fitness.png
        └── ... (outros gráficos avançados)
```

---

## ⚙️ Extensões Sugeridas

- [ ] Adicionar mapeamento lógico com inferência proposicional.
- [ ] Expandir o fitness do algoritmo genético.
- [x] Implementar logging das execuções.
- [x] Adicionar benchmarks entre agentes.
- [x] Visualização de gráficos avançados e análise de desempenho.

---

## 📚 Referências

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*  
- Wumpus World (ambiente clássico de IA simbólica)
- Algoritmos Genéticos (Holland, Goldberg)

---

## 👩‍💻 Autoria

Este projeto foi desenvolvido por [**Alfa Marine**](https://github.com/alfa-m) e [**Ingrid Mendes**](https://github.com/ingrid-kiki), com foco em pesquisa e ensino de Inteligência Artificial e Jogos Digitais.

---