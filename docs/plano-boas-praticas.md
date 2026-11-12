# Plano de implantação de boas práticas

Plano de 09/11/2026. Relaciona-se com o [plano de ação](plano-de-acao.md) original e com a [#42](https://github.com/ingrid-kiki/wumpus_world_modular/issues/42).

**Status em 11/11/2026:** Etapas 0, 1 e 2 concluídas; v1.8.0 lançada como base antes da refatoração; Etapa 3 em andamento (antecipada; PRs A a F concluídas, próxima: PR G, nomes e acentos), com a comparação final da tese depois dela.

## Objetivo

Deixar o projeto mais legível, bem documentado e eficiente: código limpo, documentação com diagramas de classes, sequência e
caso de uso, fluxogramas, código comentado para aprendizado e etapas do processo otimizadas.

## Regras para todas as etapas

- **Resultados iguais.** Limpeza e documentação não podem mudar vitórias, mortes nem gráficos. A Etapa 1 cria um teste de referência para garantir isso.
- **PRs pequenas, uma por assunto.** Mesclar antes de abrir a próxima, para não empilhar.
- **Tudo medido.** Cada etapa tem uma meta verificável.

## Estado atual (medido em 09/11/2026)

| Indicador | Hoje |
|---|---|
| Funções (sem testes e `pygad/`) | 115 |
| Funções sem docstring | 60 (52%) |
| Funções com anotação de tipos | 0 |
| Funções com mais de 30 linhas | 16; as maiores têm 148, 95 e 91 linhas |
| Funções muito complexas (C901 > 10) | 2: `gerar_graficos_avancados` e `draw_world` |
| Linhas de comentário | 17% |
| Lista de ações repetida | em 4 arquivos; agentes disponíveis em 6; 5 benchmarks quase iguais |
| Diagramas | só um diagrama de classes, na análise inicial, já desatualizado |
| Cobertura de testes | não medida (131 testes) |
| Tempo do CI | cerca de 2 min por PR |

## Etapas

### Etapa 0. Pré-requisitos (concluída)
- Mesclar as PRs #46 a #49 e lançar a v1.7.0.

### Etapa 1. Padrões e medição (concluída)
A base que protege todo o resto.

- **Teste de referência:** um benchmark fixo cujos resultados não podem mudar sem decisão explícita.
- **Cobertura de testes:** `pytest-cov` no CI, com o valor inicial como mínimo.
- **Formatação e lint:** `ruff format` e mais regras (imports, simplificações, complexidade, nomes).
- **`pre-commit`:** as mesmas checagens antes de cada commit.
- **Guia de estilo no CONTRIBUTING:** nomes, tamanho de função, docstrings e comentários.

**Meta:** CI com cobertura e lint ampliado, tudo verde.

**Divisão em tarefas (a PR A vem primeiro, porque protege as demais):**

| PR | Tarefa | Tempo previsto | Situação |
|---|---|---|---|
| A | 1.1 Definir o cenário de referência (agentes, tamanhos, sementes e parâmetros) | 10 min | Concluída (#53) |
| A | 1.2 Gerar e guardar os valores esperados (vitórias, mortes, sobrevivências e erros; só números, porque os PNGs mudam entre Windows e Linux) | 15 min | Concluída (#53) |
| A | 1.3 Criar o teste que compara com esses valores e explicar como atualizar numa mudança intencional | 20 min | Concluída (#53) |
| A | 1.4 Medir a cobertura atual com `pytest-cov` | 10 min | Concluída (#53) |
| A | 1.5 Colocar a cobertura no CI, com o valor atual como mínimo | 15 min | Concluída (#53) |
| B | 1.6 Aplicar `ruff format` num commit só de formatação | 15 min | Concluída (#54) |
| B | 1.7 Aplicar as correções automáticas (imports, espaços, sintaxe antiga) | 15 min | Concluída (#54) |
| C | 1.8 Corrigir à mão os avisos de possíveis erros e simplificações | 30 min | Concluída (#55) |
| C | 1.9 Ativar a regra de complexidade, com as 2 funções acima do limite como exceções até a refatoração | 15 min | Concluída (#55) |
| D | 1.10 Configurar o `pre-commit` e explicar como instalar | 30 min | Concluída (#56) |
| D | 1.11 Escrever o guia de estilo no CONTRIBUTING | 30 min | Concluída (#56) |

Os 33 números soltos no código ficam para a refatoração, depois da tese.

### Etapa 2. Documentação de arquitetura e diagramas (concluída)
Em `docs/arquitetura/`, com **Mermaid**, que o GitHub desenha direto e o git versiona como texto.

| Diagrama | Conteúdo |
|---|---|
| **Fluxograma geral** | Do menu do `main.py` aos resultados na pasta do run |
| **Fluxograma do AG** | População, avaliação, seleção, cruzamento, mutação e fim |
| **Diagrama de classes** | As 11 classes do programa e suas relações: `World`, agentes, `LogicKnowledgeBase`, `GeneticAlgorithm`, `Individual`, `AGVariante`, `Logger` e `Visualizer` |
| **Diagrama de sequência** | Um benchmark completo; uma execução do AG; um passo do agente lógico |
| **Diagrama de caso de uso** | Quem faz o quê: jogar, comparar agentes, reproduzir um run, rodar experimentos |
| **Fluxo de dados** | O que vira CSV, `.npz`, gráficos e `metadata.json` |

O Mermaid não tem um tipo próprio para caso de uso; ele é feito com um fluxograma no mesmo formato visual.
Um teste compara o diagrama de classes com o código, nos dois sentidos, para ele não ficar desatualizado sem aviso.
Os diagramas descrevem o código atual e serão revistos depois da refatoração.

**Meta:** os 6 tipos de diagrama publicados, em 8 arquivos, e ligados no README.

**Divisão em tarefas (cada PR é mesclada antes de abrir a próxima):**

| PR | Tarefa | Tempo previsto | Situação |
|---|---|---|---|
| A | 2.1 Criar `docs/arquitetura/`, com índice e convenções | 15 min | Concluída (#58) |
| A | 2.2 Criar o teste que compara o diagrama de classes com o código | 30 min | Concluída (#58) |
| B | 2.3 Diagrama de caso de uso | 25 min | Concluída (#60) |
| B | 2.4 Fluxograma geral | 40 min | Concluída (#60) |
| C | 2.5 Diagrama de classes, com as 11 classes e suas relações | 45 min | Concluída (#62) |
| D | 2.6 Fluxograma do AG | 30 min | Concluída (#64) |
| D | 2.7 Sequência de uma execução do AG | 25 min | Concluída (#64) |
| E | 2.8 Sequência de um benchmark completo | 30 min | Concluída (#65) |
| E | 2.9 Sequência de um passo do agente lógico | 25 min | Concluída (#65) |
| F | 2.10 Fluxo de dados | 30 min | Concluída (#67) |
| F | 2.11 Ligar os diagramas no README e atualizar o status do plano | 15 min | Concluída (#67) |

Os diagramas estão em [`docs/arquitetura/`](arquitetura/README.md).

### Etapa 3. Código limpo (16 a 23 h, antecipada em 11/11/2026)
É a Fase 5 do plano original e a [#42](https://github.com/ingrid-kiki/wumpus_world_modular/issues/42). Só avança com o teste de referência passando.

- Constantes únicas para ações, percepções e status (concluído, #72).
- Classe base de agente, com um contrato único para `run()` (concluído, #73).
- Um benchmark único no lugar dos 5, com as opções atuais (decidido; ver abaixo).
- Dividir as funções grandes: `gerar_graficos_avancados`, `GeneticAlgorithm.run`, `rodar_benchmark`.
- Anotações de tipos nas funções públicas.
- Nomes em português e sem acentos em identificadores, chaves, colunas e arquivos (decidido; ver abaixo).
- Decidir o destino de `pygad/`, que não é usado. `visual/` está decidido abaixo, e o `logger` saiu na #74.
- Decidir o uso do `dados_extra_AGENTE_NxN.npz`: hoje ele é gravado em todo run, mas nenhuma parte do programa o lê.
  Uma opção é gerar os gráficos avançados a partir dele, o que também ajudaria na [#29](https://github.com/ingrid-kiki/wumpus_world_modular/issues/29).
- Organizar em pacote, com `pyproject.toml` completo.

**Ajustes apontados pelo diagrama de classes (decididos em 11/11/2026; entram nas PRs B, C e F abaixo):**

| Ordem | Ajuste | Situação em 11/11/2026 | O que fazer | Tempo |
|---|---|---|---|---|
| 1 | Classe base de agente | Os 4 agentes só têm em comum `world` e `run()`; cada `run()` devolve um formato, e a lista de agentes está repetida em 6 arquivos | Criar uma classe abstrata com `world` e `run()`, um formato único de retorno, com as posições no histórico, e uma lista única de agentes | 2 a 3 h |
| 2 | `Logger` | `LogicAgent.logger` fica sempre `None`, o parâmetro `logger` do AG nunca é informado e os `.log` só repetem início e fim, que já estão no `terminal_output.txt` | Retirar o atributo, o parâmetro e os arquivos `.log`, deixando o `terminal_output.txt` como registro único | cerca de 1 h |
| 3 | `Visualizer` | Nenhum arquivo do programa o importa, e ele só desenha o estado atual do mundo | Ligar ao `--vis` nas execuções únicas, reproduzindo na janela os passos do agente depois que ele termina | 2 a 3 h |

Situação: os três estão concluídos: a classe base na #73, a retirada do `Logger` na #74 e a janela na #78, oferecida por
uma pergunta no menu, como decidido em 12/11/2026.
A classe base veio primeiro porque o `--vis` depende do histórico com as posições. Esses 5 a 7 h já estão contados na estimativa
da etapa. O teste de referência precisa continuar passando em cada ajuste, cada classe nova entra no diagrama de classes, e a saída dos
`.log` muda o conteúdo da pasta do run, então entra na v2.0.0.

**Decisões de 11/11/2026:**

- **Antecipar a etapa.** A comparação final da tese ([#31](https://github.com/ingrid-kiki/wumpus_world_modular/issues/31)),
  já com o `logico_seguro`, vem depois, no código refatorado.
- **Nomes em português**, inclusive os que hoje estão em inglês, como `World`, `agent_pos` e `draw_world`.
- **Sem acentos** em identificadores, chaves de dicionário, colunas do CSV e nomes de arquivos gerados, como `vitorias`,
  `tempo_medio` e `grafico_vitorias.png`. Mensagens para as pessoas e a documentação continuam com acentos. A regra passa a ser
  conferida automaticamente na PR G, e o `reproduzir.py` continua lendo runs antigos.
- **Um benchmark só**, com `--paralelo` e uma opção para menos mensagens. Os outros quatro arquivos saem, e `--benchmark`
  continua aceitando arquivos externos. A justificativa está em [`analise-benchmarks-2026-11.md`](analise-benchmarks-2026-11.md).
- **Em aberto:** o destino de `pygad/`, ligado à [#15](https://github.com/ingrid-kiki/wumpus_world_modular/issues/15), e o
  uso do `.npz` (PR I). A janela é oferecida por uma pergunta no menu (decidido em 12/11/2026).

**Divisão em tarefas (cada PR é mesclada antes de abrir a próxima; aprovada em 11/11/2026):**

| PR | Tarefa | Tempo previsto | Situação |
|---|---|---|---|
| A | 3.1 Constantes únicas para ações, percepções e status, e nomes para os números soltos | 1,5 a 2 h | Concluída (#72) |
| B | 3.2 Classe base de agente, formato único de retorno, com as posições no histórico, e lista única de agentes | 2 a 3 h | Concluída (#73) |
| C | 3.3 Retirar o `Logger`, o parâmetro `logger` e os arquivos `.log` | 1 h | Concluída (#74) |
| D | 3.4 Um benchmark único, com `--paralelo`; `tempo_total` passa a ser o tempo de relógio também no paralelo | 2 a 3 h | Concluída (#76) |
| E | 3.5 Dividir as 12 funções com mais de 40 linhas e retirar as exceções de complexidade | 2,5 a 3,5 h | Concluída (#77); `draw_world` fica para a F |
| F | 3.6 Ligar o `Visualizer` ao `--vis` e dividir `draw_world`, a última função longa | 2 a 3 h | Concluída (#78), com pergunta no menu |
| G | 3.7 Nomes em português, saídas sem acento e a regra que confere isso | 2 a 3 h | A fazer |
| H | 3.8 Tipos nas funções públicas | 1,5 a 2 h | A fazer |
| I | 3.9 Organizar em pacote, com `pyproject.toml` completo, e decidir o uso do `.npz` | 1,5 a 2 h | A fazer |
| J | 3.10 Lançar a v2.0.0 | 30 min | A fazer |

A ordem segue as dependências: a classe base usa as constantes, o benchmark único e o `--vis` dependem da classe base, e as funções
longas vêm depois do benchmark único. Os nomes ficam para o fim, para não criar conflitos com as outras PRs. Em cada PR, o teste de
referência e os números do `logico_seguro` garantem resultados idênticos, e os diagramas e a lista de testes acompanham o código.

Restam 4 PRs (G a J), com cerca de 6 a 8 h previstas.

**Meta:** nenhuma função acima de 40 linhas, nenhuma com complexidade acima de 10, nenhuma lista repetida. Lançamento: v2.0.0.

### Etapa 4. Código comentado para aprendizado (5 a 8 h)
Vem depois da Etapa 3, para não comentar código que vai mudar. Código limpo e comentário didático se completam assim:

- **Docstrings em todas as funções públicas**, em português: o que faz, parâmetros, retorno e um exemplo quando ajudar.
- **Comentários explicam o porquê**, não o que a linha faz: a regra do jogo, a decisão do algoritmo, a correção de uma issue.
- **`docs/guia-de-estudo.md`**: roteiro de leitura do código, na ordem certa (mundo, agentes, AG, benchmark), com os conceitos de IA de cada parte, os diagramas ao lado e exercícios sugeridos.

**Meta:** 100% das funções públicas com docstring e guia de estudo publicado.

### Etapa 5. Otimização das etapas do processo (4 a 7 h)

**Execução do programa**, a partir do que foi medido:

| Etapa | Observado | Melhoria proposta |
|---|---|---|
| Gráfico de violino | 35 de 39 s dos gráficos avançados | Amostrar as gerações, ou deixar opcional |
| Benchmark padrão | Até 12 min, em um processo só | Rodar em paralelo no fluxo principal (feito na #76: opção `--paralelo`) |
| Experimentos longos | Nenhum sinal de progresso | Barra de progresso com tempo restante |
| Saída no terminal | Cada passo de cada execução é impresso | Modo resumido como padrão nos benchmarks |
| Gráficos | Sempre gerados | Opção `--sem-graficos` para experimentos |
| Experimento interrompido | Recomeça do zero | Opção `--continuar` |

**Processo de trabalho:**

| Etapa | Melhoria proposta |
|---|---|
| Lançar uma versão | Script com os passos do CONTRIBUTING (versão, CHANGELOG, tag, Release) |
| PRs | Modelos de PR e de issue; mesclar antes de empilhar a próxima |
| Experimentos da tese | Um comando único que roda, compara e gera as tabelas do relato |

**Meta:** benchmark padrão pelo menos 3 vezes mais rápido, medido antes e depois, com resultados iguais.

## PRs do plano

Todas as PRs feitas desde a Etapa 0, na ordem. A data é a do merge no GitHub, em UTC; na coluna Etapa, a letra entre
parênteses é a da tabela de tarefas da etapa. "Plano", "Versão" e "Geral" são PRs de registro, lançamento ou regras do projeto.

| PR | Merge | Etapa | Assunto |
|---|---|---|---|
| [#50](https://github.com/ingrid-kiki/wumpus_world_modular/pull/50) | 2026-11-09 | 0 | Lança a v1.7.0 |
| [#51](https://github.com/ingrid-kiki/wumpus_world_modular/pull/51) | 2026-11-09 | Versão | Inicia o desenvolvimento da 1.8.0 |
| [#52](https://github.com/ingrid-kiki/wumpus_world_modular/pull/52) | 2026-11-09 | Geral | `CLAUDE.md` com as regras do projeto |
| [#53](https://github.com/ingrid-kiki/wumpus_world_modular/pull/53) | 2026-11-09 | 1 (A) | Teste de referência e cobertura no CI |
| [#54](https://github.com/ingrid-kiki/wumpus_world_modular/pull/54) | 2026-11-10 | 1 (B) | Formatação com `ruff` e regras de lint |
| [#55](https://github.com/ingrid-kiki/wumpus_world_modular/pull/55) | 2026-11-10 | 1 (C) | Regras de possíveis erros, simplificação e complexidade |
| [#56](https://github.com/ingrid-kiki/wumpus_world_modular/pull/56) | 2026-11-10 | 1 (D) | `pre-commit` e guia de estilo |
| [#57](https://github.com/ingrid-kiki/wumpus_world_modular/pull/57) | 2026-11-10 | Geral | Aviso de que o gancho do `pre-commit` precisa ser instalado |
| [#58](https://github.com/ingrid-kiki/wumpus_world_modular/pull/58) | 2026-11-10 | 2 (A) | Base dos diagramas e teste do diagrama de classes |
| [#59](https://github.com/ingrid-kiki/wumpus_world_modular/pull/59) | 2026-11-10 | Geral | Registro da proteção da `main` |
| [#60](https://github.com/ingrid-kiki/wumpus_world_modular/pull/60) | 2026-11-10 | 2 (B) | Caso de uso e fluxograma geral |
| [#61](https://github.com/ingrid-kiki/wumpus_world_modular/pull/61) | 2026-11-11 | Plano | Andamento das tarefas das Etapas 1 e 2 |
| [#62](https://github.com/ingrid-kiki/wumpus_world_modular/pull/62) | 2026-11-11 | 2 (C) | Diagrama de classes |
| [#63](https://github.com/ingrid-kiki/wumpus_world_modular/pull/63) | 2026-11-11 | Plano | Ajustes apontados pelo diagrama de classes |
| [#64](https://github.com/ingrid-kiki/wumpus_world_modular/pull/64) | 2026-11-11 | 2 (D) | Fluxograma e sequência do algoritmo genético |
| [#65](https://github.com/ingrid-kiki/wumpus_world_modular/pull/65) | 2026-11-11 | 2 (E) | Sequências do benchmark e do agente lógico |
| [#66](https://github.com/ingrid-kiki/wumpus_world_modular/pull/66) | 2026-11-11 | Agente lógico | Investigação do agente lógico |
| [#67](https://github.com/ingrid-kiki/wumpus_world_modular/pull/67) | 2026-11-11 | 2 (F) | Fluxo de dados; conclui a Etapa 2 |
| [#68](https://github.com/ingrid-kiki/wumpus_world_modular/pull/68) | 2026-11-11 | Agente lógico | Agente `logico_seguro` e lista dos testes |
| [#69](https://github.com/ingrid-kiki/wumpus_world_modular/pull/69) | 2026-11-12 | 3 (preparação) | Análise dos cinco arquivos de benchmark |
| [#70](https://github.com/ingrid-kiki/wumpus_world_modular/pull/70) | 2026-11-12 | Versão | Lança a v1.8.0 |
| [#71](https://github.com/ingrid-kiki/wumpus_world_modular/pull/71) | 2026-11-12 | Plano | Divisão e decisões da Etapa 3; inicia a 2.0.0 |
| [#72](https://github.com/ingrid-kiki/wumpus_world_modular/pull/72) | 2026-11-12 | 3 (A) | Ações, percepções e status em `world/constantes.py` |
| [#73](https://github.com/ingrid-kiki/wumpus_world_modular/pull/73) | 2026-11-12 | 3 (B) | Classe base `Agente` e lista única de agentes |
| [#74](https://github.com/ingrid-kiki/wumpus_world_modular/pull/74) | 2026-11-12 | 3 (C) | Retira o `Logger` e os arquivos `.log` |
| [#75](https://github.com/ingrid-kiki/wumpus_world_modular/pull/75) | 2026-11-12 | Plano | Andamento da Etapa 3 e esta tabela |
| [#76](https://github.com/ingrid-kiki/wumpus_world_modular/pull/76) | 2026-11-12 | 3 (D) | Benchmark único, com `--paralelo` e `--silencioso` |
| [#77](https://github.com/ingrid-kiki/wumpus_world_modular/pull/77) | 2026-11-12 | 3 (E) | Divide as funções longas e trava os limites num teste |
| [#78](https://github.com/ingrid-kiki/wumpus_world_modular/pull/78) | em revisão | 3 (F) | Janela que reproduz a partida, oferecida no menu |

Ao abrir uma PR deste plano, acrescente-a aqui na mesma PR.

## Ordem e esforço

| Etapa | Esforço | Risco | Depende de |
|---|---|---|---|
| 0. Pré-requisitos | Concluída | — | — |
| 1. Padrões e medição | Concluída | Baixo | Etapa 0 |
| 2. Documentação e diagramas | Concluída | Baixo | Etapa 0 |
| 3. Código limpo | Restam cerca de 6 a 8 h | **Médio** | Etapa 1 |
| 4. Código comentado | 5–8 h | Baixo | Etapa 3 |
| 5. Otimização | 4–7 h | Médio | Etapas 1 e 3 |
| **Restante** | **cerca de 15 a 23 h** | | |

As estimativas são de trabalho conjunto; revisões e o tempo de máquina dos experimentos vêm à parte.

## Relação com a tese

**Decidido em 11/11/2026: a Etapa 3 foi antecipada.** A v1.8.0 marca o código antes da refatoração, e a ordem passa a ser:

1. Etapas 0, 1 e 2: concluídas.
2. Etapa 3, com resultados idênticos garantidos pelos testes, terminando na v2.0.0.
3. Comparação final da #31, já com o `logico_seguro`, e novos experimentos da tese, na v2.0.0.
4. Etapas 4 e 5.

A decisão anterior, de 09/11/2026, deixava a refatoração para depois da tese.

## Decisões necessárias

1. Identificadores em português ou inglês? **Decidido em 11/11/2026:** português, sem acentos em identificadores, chaves, colunas e
   nomes de arquivos.
2. Bloquear merge com CI falho? **Decidido:** sim, com a `main` protegida desde 09/11/2026.
