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
│   ├── reprodutibilidade.py  # metadata.json de cada execução
│   └── versao.py         # Versão do projeto (fonte única)
│
├── docs/                 # Análises, plano de ação e relato das decisões (comece por docs/README.md)
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
├── benchmark.py               # Benchmark único, usado pelo main.py (sequencial ou --paralelo)
├── main.py                    # Script principal para execução
├── reproduzir.py              # Refaz um run a partir do metadata.json e compara
├── CHANGELOG.md               # Histórico de versões
├── CONTRIBUTING.md            # Como contribuir (branches, commits, versões)
└── README.md                  # Este arquivo
```

---

## 🏗️ Arquitetura

Os diagramas de caso de uso, classes, fluxogramas, sequências e fluxo de dados estão em
[`docs/arquitetura/`](docs/arquitetura/README.md).

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
ruff format .
```

Para ver a cobertura de testes: `python -m pytest --cov --cov-report=term`. O que cada teste verifica está em
[`docs/testes.md`](docs/testes.md).

Para quem vai contribuir: o gancho do `pre-commit` não vem ativado ao clonar. Rode `pre-commit install` uma vez em cada
clone, como explicado em [CONTRIBUTING.md](CONTRIBUTING.md#checagem-automática-antes-do-commit).

O [teste de referência](tests/referencia.py) garante que os resultados não mudam sem uma decisão explícita.

Os bugs corrigidos na reorganização (issues #18 a #24) têm testes de regressão em
[`tests/test_bugs_conhecidos.py`](tests/test_bugs_conhecidos.py). O CI roda os testes em cada push e PR para a `main`.

---

## 🚀 Como Executar

> 📘 **O [tutorial de uso](tutorial_execucao.md) cobre, passo a passo, tudo o que funciona hoje**, com exemplos reais,
> onde ficam os resultados, quanto tempo leva e o que ainda não funciona.

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
`--agentes genetico --sizes 4 6 8 --execucoes 50 --populacao 100 --geracoes 500 --cromossomo 100`.

| Opção | Padrão | Descrição |
|---|---|---|
| `--execucoes` | 32 | Execuções por agente e tamanho (a execução *i* usa a semente *i*) |
| `--sizes` | 4 6 8 | Tamanhos do mundo |
| `--agentes` | logico genetico | Agentes do benchmark |
| `--benchmark` | benchmark.py | Arquivo de benchmark (os 5 do projeto são compatíveis) |
| `--populacao`, `--geracoes`, `--cromossomo` | 100, 500, 100 | Parâmetros do agente genético |
| `--mutacao`, `--cruzamento` | 0,02, 0,8 | Taxas do agente genético |
| `--proximidade` | 0 | Peso do bônus de proximidade ao ouro no fitness (0 = fitness original) |
| `--avaliacoes` | população × gerações | Orçamento da busca aleatória (agente `aleatorio`) |
| `--saida` | `logs/run_AAAAMMDD_HHMMSS` | Pasta de saída |

Antes, os parâmetros do genético só podiam ser mudados editando `agents/genetic_agent.py`.

### 🔁 Reproduzir uma execução

Todo benchmark grava um `metadata.json` na pasta do run com tudo o que é preciso para refazê-lo: versão e commit
do código (e se havia alterações não commitadas), argumentos, parâmetros efetivos do genético, regra das sementes
e versões do Python e das bibliotecas. Para refazer e comparar:

```bash
python reproduzir.py logs/run_AAAAMMDD_HHMMSS
```

O script avisa se o commit, a versão ou as bibliotecas forem diferentes e compara vitórias, mortes e
sobrevivências, que precisam ser idênticas. Tempos, memória e CPU variam de máquina para máquina e não entram na
comparação. Runs anteriores à v1.5.0 não têm `metadata.json`.

### 🔧 Uma partida com janela

As opções 2, 3 e 4 do menu jogam uma partida e, no fim, perguntam "Ver a partida numa janela? (s/N)". Respondendo `s`,
uma janela reproduz a partida passo a passo. Para fechar, use o botão da janela.

```bash
python main.py
```

A sintaxe `python main.py logico --size 4 --vis`, prometida em versões anteriores deste README, nunca existiu: as
execuções únicas são escolhidas pelo menu.

---

## 🧠 Tipos de Agentes

| Tipo      | Descrição |
|-----------|-----------|
| `manual`  | Agente controlado pelo teclado do usuário. |
| `logico`  | Agente baseado em lógica simbólica simples (regras IF/ELSE). |
| `logico_seguro` | Agente lógico que deduz quais casas não têm poço antes de andar e só arrisca quando não há casa segura. |
| `genetico`| Agente baseado em algoritmo genético com avaliação de desempenho. |
| `aleatorio` | Busca aleatória com o mesmo orçamento do genético, usada como referência para ele. |

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
| Proximidade ao ouro (só com `--proximidade P`) | de 0 a +P, pela menor distância alcançada |

Sem semente explícita, o AG usa a semente do mundo: o mesmo mundo produz sempre a mesma evolução.

---

## 🖼️ Interface Visual

Oferecida no fim das opções 2, 3 e 4 do menu, a janela (`visual/visualizer.py`) refaz a partida passo a passo e mostra:

- 🟥 Wumpus  
- 🕳️ Poços  
- 🟡 Ouro  
- 🟢 Agente  
- 📣 Grito (se o Wumpus morrer)  
- ☠️ Morte do agente  
- 🏆 Vitória (pegou o ouro)
- As percepções de cada casa (brisa, fedor, brilho) e a ação de cada passo

---

## 📊 Benchmarks e Gráficos

Compare o desempenho dos agentes de forma automatizada, com resultados organizados em subpastas de `/logs` e geração de gráficos básicos e avançados.

### Pelo `main.py` (recomendado)
Escolha a opção 1 do menu, passando as opções na linha de comando, ou use a opção 5 e digite as opções:
```bash
python main.py --execucoes 30 --sizes 4 6 8 --agentes logico logico_seguro genetico --paralelo
```

- `--paralelo` roda as execuções em processos paralelos. Compensa em runs longos: o benchmark padrão levou 102 s em
  paralelo e 258 s em sequência. Em runs curtos, iniciar os processos custa alguns segundos a mais.
- `--silencioso` esconde as mensagens de cada execução e de cada passo dos agentes.
- Os resultados são os mesmos nos dois modos.

### Teste rápido
Executa 3 rodadas em 4x4 de cada agente automático e mostra só o resumo:
```bash
python benchmark.py
```

Até a v1.8.0 havia mais quatro arquivos de benchmark (`benchmark_custom.py`, `benchmark_fast.py`, `benchmark_graficos.py` e
`benchmark_sideB.py`). Eles davam os mesmos resultados e foram trocados pelas opções acima; a justificativa está em
[`docs/analise-benchmarks-2026-11.md`](docs/analise-benchmarks-2026-11.md).

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
    ├── metadata.json                      # Versão, commit, argumentos e bibliotecas (para reproduzir)
    ├── resultados_benchmark.csv           # Só colunas escalares
    ├── dados_extra_genetico_4x4.npz       # Arrays do AG (fitness, diversidade, memória, CPU...)
    ├── terminal_output.txt                # Saída completa do terminal
    ├── grafico_vitórias.png
    ├── grafico_mortes.png
    ├── grafico_sobreviveu.png
    ├── grafico_tempo_medio.png
    └── advanced_charts_genetico_4x4/     # ← Gráficos avançados por agente/tamanho
        ├── convergencia_populacao.png
        ├── evolucao_fitness.png
        └── heatmap_diversidade.png
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

O histórico das decisões do projeto está em [`docs/`](docs/README.md), incluindo o relato da
[reorganização de novembro de 2026](docs/reorganizacao-2026-11.md).

### 🛠️ Ferramentas utilizadas

As ferramentas abaixo foram cruciais para elaborar, revisar e evoluir este trabalho. **Elas não são autoras**: não
são pessoas. As decisões, a revisão e a responsabilidade pelo conteúdo são das autoras.

| Ferramenta | Como foi usada |
|---|---|
| [Visual Studio Code](https://code.visualstudio.com/) | Ambiente de desenvolvimento do projeto (configuração em `wumpus_CE_2025.code-workspace`). |
| [GitHub Copilot](https://github.com/features/copilot) | Assistente de programação no editor durante a escrita do código. |
| [Claude Code](https://claude.com/claude-code) | Assistente de programação na reorganização de novembro de 2026 (v1.4.0 e v1.5.0): análise do código, testes, correção de bugs, versionamento e documentação, sempre com revisão e aprovação das autoras. |

Por isso, nenhuma delas é registrada como coautora. Os commits de 06/11/2026 que ainda trazem
`Co-Authored-By: Claude` serão corrigidos na reescrita do histórico prevista em
[#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17).

---