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
├── exemplos/             # Resumo dos 34 experimentos do AG + galeria de gráficos
│   ├── README.md
│   └── galeria/
│
├── pygad/                # Implementação alternativa com PyGAD (requer WumpsimAG, não incluso)
│
├── logs/                 # Criada ao rodar; NÃO versionada (ver .gitignore)
│   └── run_YYYYMMDD_HHMMSS/   # Subpastas por execução, com CSVs, PNGs e logs
│      └── advanced_charts_agent_size/   # Resultados dos gráficos avançados
│
├── benchmark.py               # Benchmark padrão (4x4)
├── benchmark_custom.py        # Benchmark customizável via argumentos
├── benchmark_fast.py          # Benchmark paralelo, organizado por pastas
├── benchmark_graficos.py      # Benchmark com geração automática de gráficos
├── benchmark_sideB.py         # Benchmark alternativo para comparação
├── main.py                    # Script principal para execução
├── CHANGELOG.md               # Histórico de versões
├── CONTRIBUTING.md            # Como contribuir (branches, commits, versões)
└── README.md                  # Este arquivo
```

---

## 🧪 Requisitos

- Python 3.12 ou superior (testado em 3.12 e 3.13; o numpy 2.5 exige 3.12, ver [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17))
- Dependências com versões fixadas em [`requirements.txt`](requirements.txt): pygame, matplotlib, pandas, joblib, seaborn, scikit-learn, numpy, psutil e pygad

### Instalação de dependências

```bash
python -m venv .venv
pip install -r requirements.txt
```

### Testes

```bash
pip install -r requirements-dev.txt
python -m pytest
ruff check .
```

Os bugs corrigidos na reorganização (issues #18 a #24) têm testes de regressão em
[`tests/test_bugs_conhecidos.py`](tests/test_bugs_conhecidos.py). O CI roda os testes em cada push e PR para `main` e `reorg/v2`.

---

## 🚀 Como Executar

🎮 Menu Interativo (Novo)
Execute o programa principal para acessar o menu interativo:

1 - Benchmark (vários agentes e tamanhos)
2 - Agente Manual (interativo)
3 - Agente Lógico (uma execução)
4 - Agente Genético (uma execução)
5 - Customizado via linha de comando (CLI)

```bash
python main.py
```

Na opção 5, digite os argumentos do benchmark, por exemplo:
`--agentes genetico --sizes 4 6 8 --execucoes 50`.

### 🔧 Sintaxe

> ⚠️ **Ainda não implementado.** A sintaxe abaixo é a planejada para a v2.0.0
> (ver [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17)).
> Hoje o `main.py` só abre o menu interativo e ignora esses argumentos, e o `--vis` não está ligado ao `Visualizer`.

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

### ⚖️ Os agentes não jogam nas mesmas condições

- O **agente lógico** só conhece o que percebe: decide passo a passo a partir de `FEDOR`, `BRISA` e `BRILHO`.
  Ele tem um limite de `4 × N²` passos; se não vencer nem morrer até lá, conta como "sobreviveu".
- O **agente genético** planeja *antes* de jogar: avalia milhares de sequências de ações simulando cópias do
  mundo real (`world.clone()`), ou seja, conhece indiretamente onde estão o Wumpus, os poços e o ouro.
  Depois executa a melhor sequência encontrada.

Por isso, comparar as taxas de vitória dos dois mede "planejar com o mapa" contra "reagir às percepções",
e não qual algoritmo é melhor em igualdade de informação.

---

## 📜 Regras deste Wumpus World

Este projeto usa uma versão simplificada do ambiente clássico (Russell & Norvig). As diferenças são intencionais
e afetam os resultados:

| Regra | Neste projeto | Clássico |
|---|---|---|
| Mundo | Grid N×N; o agente começa em (0,0) | 4×4 |
| Poços | Exatamente `N // 2`, em casas diferentes, nunca no início, no ouro ou no Wumpus | 20% de chance por casa |
| Ações | `CIMA`, `BAIXO`, `ESQUERDA`, `DIREITA`, `AGARRAR`, `TIRO` (sem girar) | Girar, avançar, agarrar, atirar, sair |
| Percepções | `FEDOR` (Wumpus adjacente e vivo), `BRISA` (poço adjacente), `BRILHO` (ouro na casa) | Também `IMPACTO` e `GRITO` |
| Parede | O movimento é ignorado, sem percepção de impacto | Percepção `IMPACTO` |
| Tiro | Flechas ilimitadas; sem direção: mata o Wumpus se ele estiver em qualquer casa adjacente | Uma flecha, em linha reta |
| Vitória | Agarrar o ouro termina o jogo | Agarrar o ouro e voltar a (0,0) |
| Fim de jogo | Depois de vencer ou morrer, nenhuma ação tem efeito | — |
| Aleatoriedade | `World(N, seed)` usa um gerador próprio; a mesma semente gera sempre o mesmo mundo | — |

### Fitness do agente genético

Cada cromossomo é uma sequência de ações executada numa cópia do mundo:

| Evento | Pontos |
|---|---:|
| Movimento | −0,5 |
| `AGARRAR` ou `TIRO` | −1 |
| Agarrar o ouro (fim de jogo) | +100 |
| Tiro que mata o Wumpus | +25 |
| Morrer (fim de jogo) | −100 |
| Terminar vivo | +10 |

Sem semente explícita, o AG usa a semente do mundo: o mesmo mundo produz sempre a mesma evolução.

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

A pasta `logs/` **não é versionada**: cada pessoa gera a sua ao rodar. Para compartilhar resultados,
anexe o zip do run a um GitHub Release (ver [CONTRIBUTING.md](CONTRIBUTING.md)).
Os experimentos de julho/2025 estão resumidos em [`exemplos/README.md`](exemplos/README.md), e os dados completos
estão no Release [`v1.3.0-dados`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.3.0-dados).

Os arquivos de log são salvos automaticamente em subpastas de `/logs/`, organizados por execução e agente:

```
/logs/
└── run_YYYYMMDD_HHMMSS/
    ├── resultados_benchmark.csv
    ├── terminal_output.txt                # ← NOVO: Saída completa do terminal
    ├── logico_YYYYMMDD_HHMMSS.log        # ← Logs detalhados por agente
    ├── genetico_YYYYMMDD_HHMMSS.log      # ← Logs detalhados por agente
    ├── grafico_vitorias.png
    ├── grafico_mortes.png
    ├── grafico_sobreviveu.png
    ├── grafico_tempo_medio.png
    └── advanced_charts_genetico_4x4/     # ← Gráficos avançados por agente/tamanho
        ├── convergencia_populacao.png
        ├── evolucao_fitness.png
        └── performance_heatmap.png
```

---
## 💾 Captura de Terminal (Novo)

Toda a saída do terminal é automaticamente capturada e salva em terminal_output.txt, permitindo:

- Análise posterior dos resultados completos
- Rastreabilidade de todas as execuções
- Debugging mais eficiente
- Documentação automática de experimentos

---
## ⏱️ Formatação Inteligente de Tempo (Novo)

O projeto agora formata automaticamente os tempos de execução:

Segundos para tempos < 60s: "45.23s"
Minutos para tempos ≥ 60s: "2.34 min"
Exemplo de saída:

📊 RESULTADOS - GENETICO | Tamanho: 6x6
🏆 Vitórias: 15 (75.0%)
☠️ Mortes: 3 (15.0%)
🤔 Sobreviveu sem vencer: 2 (10.0%)
⏱️ Tempo total: 2.45 min | Tempo médio: 7.35s

---
## 🛡️ Tratamento de Erros (Novo)

O sistema agora inclui tratamento robusto de erros:

- Try/catch nas execuções dos agentes
- Validação de resultados antes de processar
- Logs de erro detalhados
- Continuidade da execução mesmo com falhas individuais

---

## ⚙️ Extensões Sugeridas

- [ ] Adicionar mapeamento lógico com inferência proposicional.
- [ ] Expandir o fitness do algoritmo genético.
- [x] Implementar logging das execuções.
- [x] Adicionar benchmarks entre agentes.
- [x] Visualização de gráficos avançados e análise de desempenho.
- [x] Menu interativo para facilitar o uso.
- [x] Captura automática da saída do terminal.
- [x] Formatação inteligente de tempo.

---

## 📚 Referências

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*  
- Wumpus World (ambiente clássico de IA simbólica)
- Algoritmos Genéticos (Holland, Goldberg)

---

## 👩‍💻 Autoria

Este projeto foi desenvolvido por [**Alfa Marine**](https://github.com/alfa-m) e [**Ingrid Mendes**](https://github.com/ingrid-kiki), com foco em pesquisa e ensino de Inteligência Artificial e Jogos Digitais.

---