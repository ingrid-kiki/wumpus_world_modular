# Plano de implantação de boas práticas

Plano de 09/11/2026. Relaciona-se com o [plano de ação](plano-de-acao.md) original e com a [#42](https://github.com/ingrid-kiki/wumpus_world_modular/issues/42).

**Status em 09/11/2026:** Etapa 0 concluída com a v1.7.0; Etapa 1 concluída (PRs A a D); Etapa 2 em andamento (PRs A a C concluídas; próxima: PR D, fluxograma e sequência do AG).

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

### Etapa 2. Documentação de arquitetura e diagramas (4 a 6 h, em andamento)
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
| D | 2.6 Fluxograma do AG | 30 min | A fazer |
| D | 2.7 Sequência de uma execução do AG | 25 min | A fazer |
| E | 2.8 Sequência de um benchmark completo | 30 min | A fazer |
| E | 2.9 Sequência de um passo do agente lógico | 25 min | A fazer |
| F | 2.10 Fluxo de dados | 30 min | A fazer |
| F | 2.11 Ligar os diagramas no README e atualizar o status do plano | 15 min | A fazer |

Restam 3 PRs (D a F), com cerca de 2 h 35 previstas.

### Etapa 3. Código limpo (10 a 18 h)
É a Fase 5 do plano original e a [#42](https://github.com/ingrid-kiki/wumpus_world_modular/issues/42). Só avança com o teste de referência passando.

- Constantes únicas para ações, percepções e status.
- Classe base de agente, com um contrato único para `run()`.
- Um runner único no lugar dos 5 benchmarks, com as opções atuais.
- Dividir as funções grandes: `gerar_graficos_avancados`, `GeneticAlgorithm.run`, `rodar_benchmark`.
- Anotações de tipos nas funções públicas.
- Nomes em um idioma só e sem acentos em chaves e arquivos.
- Decidir o destino do código sem uso: `visual/`, `pygad/` e o parâmetro `logger`.
- Organizar em pacote, com `pyproject.toml` completo.

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
| Benchmark padrão | Até 12 min, em um processo só | Rodar em paralelo no fluxo principal (`benchmark_fast` já faz isso) |
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

## Ordem e esforço

| Etapa | Esforço | Risco | Depende de |
|---|---|---|---|
| 0. Pré-requisitos | Concluída | — | — |
| 1. Padrões e medição | Concluída | Baixo | Etapa 0 |
| 2. Documentação e diagramas | Restam cerca de 2 h 35 | Baixo | Etapa 0 |
| 3. Código limpo | 10–18 h | **Médio** | Etapa 1 |
| 4. Código comentado | 5–8 h | Baixo | Etapa 3 |
| 5. Otimização | 4–7 h | Médio | Etapas 1 e 3 |
| **Restante** | **cerca de 22 a 36 h** | | |

As estimativas são de trabalho conjunto; revisões e o tempo de máquina dos experimentos vêm à parte.

## Relação com a tese

**Decidido em 09/11/2026: a refatoração fica para depois da tese.** A Etapa 3 mexe em quase todos os arquivos, então a ordem é:

1. Etapas 0, 1 e 2: seguras, e os diagramas já servem para a tese.
2. Comparação final da #31 e novos experimentos da tese.
3. Etapas 3, 4 e 5, depois que os números da tese estiverem fechados.

## Decisões necessárias

1. Identificadores em português ou inglês? Hoje estão misturados. Minha sugestão é português, como o resto do projeto. Só afeta a Etapa 3.
2. Bloquear merge com CI falho? **Decidido:** sim, com a `main` protegida desde 09/11/2026.
