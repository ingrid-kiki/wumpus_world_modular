# 🧠 Wumpus World com Agentes Inteligentes

Este projeto simula o clássico **Wumpus World** com suporte a **diferentes tipos de agentes inteligentes** (manual, lógico e genético), e inclui uma interface visual interativa com **Pygame**.

> 💡 Ideal para fins didáticos, estudo de IA simbólica, algoritmos genéticos e jogos baseados em agentes.

---

## 🎯 Objetivos

- Explorar diferentes estratégias de tomada de decisão em ambientes incertos.
- Comparar abordagens **manuais**, **baseadas em lógica simbólica** e **algoritmos genéticos**.
- Visualizar o ambiente e as ações dos agentes em tempo real.

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
├── main.py               # Script principal para execução
└── README.md             # Este arquivo
```

---

## 🧪 Requisitos

- Python 3.8 ou superior
- Pygame

### Instalação de dependências

```bash
pip install pygame matplotlib pandas joblib
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

Compare o desempenho dos agentes de forma automatizada:

Benchmark Padrão
Executa 20 rodadas para cada agente:
```bash
python benchmark.py
```

Benchmark Customizado
Permite definir número de execuções, tamanhos de mundo e agentes:
```bash
python benchmark_custom.py --execucoes 30 --sizes 4 6 8 --agentes logico genetico
```

Benchmark Alternativo
Executa benchmarks em diferentes tamanhos de mundo (4x4, 6x6, 8x8):
```bash
python benchmark_sideB.py 
```
Benchmark com Gráficos
Gera relatórios em CSV e gráficos automáticos (requer pandas, matplotlib e joblib):
```bash
python benchmark_graficos.py --execucoes 20 --sizes 4 6 8 --agentes logico genetico
```
Os gráficos e resultados serão salvos como arquivos PNG e CSV no diretório do projeto.

---

## 📁 Logs
Os arquivos de log são salvos automaticamente na pasta /logs/:

```
/logs/
├── logico_YYYYMMDD_HHMMSS.log
├── genetico_YYYYMMDD_HHMMSS.log
```

---

## ⚙️ Extensões Sugeridas

- [ ] Adicionar mapeamento lógico com inferência proposicional.
- [ ] Expandir o fitness do algoritmo genético.
- [ ] Implementar logging das execuções.
- [ ] Adicionar benchmarks entre agentes.
- [ ] Visualização da árvore de decisão.

---

## 📚 Referências

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*  
- Wumpus World (ambiente clássico de IA simbólica)
- Algoritmos Genéticos (Holland, Goldberg)

---

## 👩‍💻 Autoria

Este projeto foi desenvolvido por **Alfa Marine** e **Ingrid Mendes**, com foco em pesquisa e ensino de Inteligência Artificial e Jogos Digitais.

---