# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/).
Veja as regras em [CONTRIBUTING.md](CONTRIBUTING.md).

## [Não lançado]

Próximas etapas em [`docs/plano-boas-praticas.md`](docs/plano-boas-praticas.md).

### Adicionado
- Regra automática contra acentos em nomes: o `ruff` (regras `PLC2401` e `PLC2403`) confere os nomes do código, e
  `tests/test_nomes_sem_acento.py`, os textos usados como nome e tudo o que um run grava.
- Opções `--paralelo` e `--silencioso` no `main.py`. `--paralelo` roda as execuções em processos paralelos (o benchmark padrão
  levou 102 s, contra 258 s em sequência); `--silencioso` esconde as mensagens de cada execução e de cada passo. Os resultados
  são os mesmos nos dois modos.
- Janela que reproduz a partida passo a passo, oferecida no fim das opções 2, 3 e 4 do menu ("Ver a partida numa janela?").
  O `Visualizer` (hoje `Visualizador`) existia, mas não estava ligado ao programa; agora refaz a partida a partir do estado inicial do mundo.

### Alterado
- **Os nomes do código estão em português**: classes, métodos, atributos, parâmetros e variáveis. Quem importa o código
  precisa usar os nomes novos; os nomes dos arquivos `.py` e das pastas mudam na organização em pacote. Os principais:

  | Até a v1.8.0 | Agora |
  |---|---|
  | `World`, com `size`, `seed`, `agent_pos`, `gold_pos`, `wumpus_pos`, `pits`, `is_alive`, `won` | `Mundo`, com `tamanho`, `semente`, `posicao_agente`, `posicao_ouro`, `posicao_wumpus`, `pocos`, `agente_vivo`, `ganhou` |
  | `World.step`, `perceive`, `clone`, `is_done` | `Mundo.agir`, `perceber`, `clonar`, `terminou` |
  | `run()` dos agentes e do algoritmo genético | `executar()` |
  | `LogicAgent`, `GeneticAgent`, `ManualAgent`, `RandomSearchAgent` | `AgenteLogico`, `AgenteGenetico`, `AgenteManual`, `AgenteAleatorio` |
  | `LogicKnowledgeBase` e `infer_action` | `BaseConhecimento` e `inferir_acao` |
  | `GeneticAlgorithm`, com `pop_size`, `gens`, `chrom_length`, `mutation_rate`, `crossover_rate` | `AlgoritmoGenetico`, com `tamanho_populacao`, `geracoes`, `tamanho_cromossomo`, `taxa_mutacao`, `taxa_cruzamento` |
  | `Individual`, com `chromosome` e `evaluate` | `Individuo`, com `cromossomo` e `avaliar` |
  | `Visualizer` | `Visualizador` |

  No `metadados.json`, os parâmetros do agente genético passam a usar os nomes novos (`tamanho_populacao`, `geracoes`...).
  As opções de linha de comando não mudam. Os resultados também não: o teste de referência passa, e o mesmo benchmark deu
  contagens, `.npz`, 19 gráficos e saída do terminal idênticos.
- **As saídas não têm mais acento e estão em português.** Os números e os gráficos são os mesmos; mudam só os nomes:

  | Até a v1.8.0 | Agora |
  |---|---|
  | colunas `vitórias` e `tempo_médio` do CSV | `vitorias` e `tempo_medio` |
  | status `vitória` de cada execução | `vitoria` |
  | `metadata.json` | `metadados.json` |
  | `terminal_output.txt` | `saida_terminal.txt` |
  | pasta `advanced_charts_AGENTE_NxN/` | `graficos_avancados_AGENTE_NxN/` |
  | `grafico_vitórias.png` | `grafico_vitorias.png` |
  | `curva_convergencia_std.png`, `violin_fitness.png` e `heatmap_diversidade.png` | `curva_convergencia_desvio_padrao.png`, `violino_fitness.png` e `mapa_de_calor_diversidade.png` |
  | opção `--sizes` | `--tamanhos` |

  O `reproduzir.py` continua refazendo runs gravados até a v1.8.0: ele lê o `metadata.json`, troca `--sizes` por
  `--tamanhos`, traduz as colunas antigas e usa o `benchmark.py` no lugar dos quatro benchmarks retirados, que davam os
  mesmos resultados. Dois runs reais da v1.6.0, um deles feito com o `benchmark_fast.py`, foram refeitos com resultados
  idênticos.
- Ações, percepções e status do jogo ficam num lugar só, `world/constantes.py`, e os números das regras do fitness e do AG
  ganham nomes. Um teste impede que essas listas voltem a ser escritas à mão. Os resultados não mudam.
- **Todos os agentes herdam da classe base `Agente`** (`agents/agente.py`), e `run()` devolve um formato único:
  `historico`, `passos` e `dados_extra`. Cada passo do histórico traz `passo`, `acao`, `percepcao`, `status` e `posicao`;
  antes as chaves eram `history`, `ação` e `perception`, e o agente lógico não registrava as ações. A lista de agentes passa a
  existir só em `agents/registro.py`. As jogadas são as mesmas: a referência foi regenerada só por causa do formato.
- `tempo_total` passa a ser o tempo de relógio de cada combinação de agente e tamanho, também no modo paralelo; antes, no
  paralelo, era a soma do tempo das execuções. `tempo_medio` continua sendo a média do tempo de cada execução.
- As funções longas foram divididas: nenhuma função do programa passa de 40 linhas nem tem
  complexidade acima de 10, sem exceções (a última, `draw_world`, foi dividida junto com a janela). Os gráficos gerados são idênticos byte a byte, e os resultados não mudam.

### Removido
- O `Logger` (`utils/logger.py`), o atributo `logger` do agente lógico, o parâmetro `logger` de `GeneticAlgorithm.run` e os
  arquivos `AGENTE_AAAAMMDD_HHMMSS.log` da pasta do run. Eles só repetiam o início e o fim de cada combinação, que continuam
  no `terminal_output.txt`, o registro único de cada run. Os resultados não mudam.
- `benchmark_custom.py`, `benchmark_fast.py`, `benchmark_graficos.py` e `benchmark_sideB.py`. Davam os mesmos resultados do
  `benchmark.py`, que passa a ser o único; o que tinham de próprio virou `--paralelo` e `--silencioso`
  ([análise](docs/analise-benchmarks-2026-11.md)).
- A pasta `pygad/`, que não rodava sem o módulo `WumpsimAG`, ausente do projeto. Ela está guardada na tag
  `archive/pygad-original` para ser retomada na [#15](https://github.com/ingrid-kiki/wumpus_world_modular/issues/15). A biblioteca `pygad` continua nas dependências.

### Corrigido
- No Windows, redirecionar a saída para um arquivo (`python main.py > saida.txt`) ou lê-la de outro programa derrubava o
  `main.py`, o `reproduzir.py`, o `benchmark.py` e os experimentos com `UnicodeEncodeError`, porque a codificação usada
  (cp1252) não tem emojis. Os scripts passam a saída para UTF-8 ao começar (`utils/terminal.py`).

### Documentação
- README e LICENSE sem as inconsistências da [#41](https://github.com/ingrid-kiki/wumpus_world_modular/issues/41): a LICENSE passa a citar as duas autoras, o README
  explica como ativar o `.venv` e descreve a janela como ela é, e os títulos "(Novo)" saíram.
- `CLAUDE.md`, `CONTRIBUTING.md` e o plano de boas práticas exigem que toda PR atualize o histórico e os planos.

---

## [1.8.0] - 2026-11-11

Última versão antes da refatoração da Etapa 3 do plano de boas práticas, que levará à v2.0.0. Os resultados dos agentes
`logico`, `genetico` e `aleatorio` são **idênticos** aos da v1.7.0 para os mesmos parâmetros e sementes; o teste de referência
garante isso. A novidade nos resultados é o agente `logico_seguro`.

### Adicionado
- Agente `logico_seguro`: deduz quais casas não têm poço antes de andar e só arrisca quando não há casa segura nova.
  Venceu 83,4%, 86,4% e 91,9% dos mundos 4x4, 6x6 e 8x8, contra 33,3%, 24,2% e 19,4% do `logico`, que não muda.
  Detalhes em [`docs/investigacao-agente-logico-2026-11.md`](docs/investigacao-agente-logico-2026-11.md).
- Lista dos testes automáticos em [`docs/testes.md`](docs/testes.md), com o que cada um garante. O teste
  `tests/test_lista_de_testes.py` falha quando a lista fica desatualizada.
- Teste de referência (`tests/test_referencia.py`): mundos, sequências de ações e regras do fitness não podem mudar
  sem decisão explícita.
- Cobertura de testes no CI com `pytest-cov`: 79% hoje, mínimo de 78%.
- Padronização com `ruff format`, verificada no CI, e regras de lint para imports, espaços e sintaxe antiga. Os commits só de
  formatação ficam em `.git-blame-ignore-revs`.
- Regras de lint para possíveis erros (`B`) e simplificações (`SIM`), e limite de complexidade 10 por função.
  `gerar_graficos_avancados` e `draw_world` ficam como exceções até a refatoração.
- Checagem automática com `pre-commit` antes de cada commit e guia de estilo no `CONTRIBUTING.md`.
- Pasta `docs/arquitetura/`, com índice e convenções, e teste que compara o diagrama de classes com o código.
- Diagramas em `docs/arquitetura/`: caso de uso, classes, fluxograma geral, fluxograma do algoritmo genético e sequências do AG, do
  benchmark e do agente lógico, e fluxo de dados. O teste do diagrama de classes confere todas as classes do programa.

### Alterado
- A `main` agora é protegida no GitHub: exige PR e o CI aprovado nos quatro ambientes, e bloqueia force-push e exclusão.
  A revisão de outra pessoa é recomendada, mas não obrigatória.
- Os comentários do agente `logico` deixam de prometer "ações seguras": ele decide com regras simples e não consulta se a casa
  é segura. O comportamento não muda.

### Documentação
- [`docs/investigacao-agente-logico-2026-11.md`](docs/investigacao-agente-logico-2026-11.md): por que o agente lógico morre em
  poços, a medição de quatro formas de decidir e a decisão de criar o `logico_seguro`.
- [`docs/analise-benchmarks-2026-11.md`](docs/analise-benchmarks-2026-11.md): os cinco arquivos de benchmark dão os mesmos
  resultados; o benchmark padrão levou 258 s em sequência e 102 s em paralelo.
- `CLAUDE.md` com as regras do projeto para o Claude Code, e plano de boas práticas com as Etapas 1 e 2 concluídas.

---

## [1.7.0] - 2026-11-09

Os resultados (vitórias, mortes, sobrevivências) são **idênticos** aos da v1.6.0 para os mesmos parâmetros e sementes,
sem usar as opções novas.

### Adicionado
- Agente `aleatorio` (busca aleatória), referência para o agente genético, com o mesmo cromossomo e o mesmo orçamento
  de avaliações ([#31]).
- `--proximidade P`: bônus opcional no fitness do AG por chegar perto do ouro. Com o padrão 0, o fitness e os
  resultados não mudam. Foi a única mudança que superou a busca aleatória com significância ([#31]).
- `experimentos/comparar_metodos.py` e `docs/investigacao-31-ag-vs-busca-aleatoria.md`: comparação pareada de métodos,
  com teste estatístico.
- Tutorial: seção "Problemas comuns no Windows".
- `docs/resumo-2026-11.md` e `docs/plano-boas-praticas.md`: resumo do trabalho de novembro de 2026 e plano de boas práticas.

### Corrigido
- **Um gráfico não interrompe mais o benchmark** ([#37]). Antes, uma falha nos gráficos avançados parava o `main.py`
  sem gravar o CSV, e as execuções já feitas se perdiam (por exemplo, com `--populacao 1`, `--geracoes 0` ou
  `--cromossomo 1 --cruzamento 0`). Agora um gráfico sem dados suficientes é pulado, com aviso, e uma falha vai para o
  stderr sem impedir os demais. Os gráficos gerados não mudam.
- **Uma interrupção não perde mais o que já foi feito.** `resultados_benchmark.csv` e os `.npz` são gravados ao fim de
  cada agente e tamanho, por substituição atômica, e `terminal_output.txt` é gravado durante a execução e registra o
  erro que interrompeu o programa, inclusive Ctrl+C. Uma queda perde no máximo a etapa em andamento.
- Os gráficos avançados passam a ser gerados para qualquer agente que devolva dados extras, e não só para `genetico`.
  A mensagem no terminal informa quantos gráficos foram realmente gerados e quais falharam.
- **Entradas inválidas** ([#38]): o mundo de tamanho 1 travava o programa; agora o tamanho mínimo é 2. As opções do
  benchmark são validadas, com mensagem clara, e o menu repete a pergunta quando o tamanho ou a semente são inválidos.
  O agente `manual` não é mais aceito em `--agentes`. O cruzamento não falha mais com cromossomo de um gene.
- Caminhos do Windows com barra invertida funcionam na opção 5 do menu ([#39]); antes, as barras eram apagadas.
- O traceback dos erros do `benchmark_fast.py` agora chega ao `terminal_output.txt` ([#40]).

### Modificado
- O comentário "NÃO ALTERAR" do `main.py` foi substituído por testes (`tests/test_main_etapas.py`) que garantem as
  pastas, os arquivos e a gravação parcial de cada etapa.

---

## [1.6.0] - 2026-11-09

Versão de manutenção. Os resultados (vitórias, mortes, sobrevivências) são **idênticos** aos da v1.5.0 para os mesmos
parâmetros e sementes; o CSV ganha a coluna `erros`.

### Corrigido
- **Erros nos benchmarks** ([#30]): os 5 benchmarks passam a tratar uma execução que falha do mesmo jeito. Ela não
  conta mais como vitória, morte ou sobrevivência (o `benchmark.py` contava como "sobreviveu" e o `benchmark_fast.py`
  descartava sem aviso), entra na nova coluna `erros`, e o benchmark continua com as demais execuções (os outros
  três paravam). Os dados extras vêm da primeira execução sem erro.
- `python benchmark.py` não testa mais o agente manual, que pedia ações pelo teclado e falhava 3 vezes sem ninguém
  digitando.
- `terminal_output.txt` passa a incluir o **stderr**: tracebacks e avisos das execuções ficam salvos na pasta do run.
- `benchmark_graficos.py` rodado sozinho grava em `logs/run_.../` (ou em `--saida`), e não mais na pasta atual.
- `benchmark_fast.py` e `benchmark_graficos.py` rodados sozinhos gravam só colunas escalares no CSV.
- Os benchmarks não anunciam mais uma estimativa de tempo fixa no código, que nunca foi medida.

### Modificado
- CI roda só em push e PR para a `main` (a branch `reorg/v2` já foi mesclada).
- `resultados_benchmark.csv` ganha a coluna `erros`. O resumo impresso mostra os erros quando há, e os percentuais
  usam o total de execuções. `reproduzir.py` compara a coluna `erros` quando os dois CSVs a têm.
- `utils/execucao.py`: `executar_uma()` e `contar()`, usadas pelos 5 benchmarks.

### Documentação
- **`tutorial_execucao.md` reescrito** com o que funciona hoje, com todos os comandos conferidos: menu, agente manual,
  opções do benchmark, resultados, `reproduzir.py`, benchmarks avulsos, tempos medidos e o que ainda não funciona.
  Saíram comandos que nunca existiram (`main.py logico --vis`, `benchmark.py --execucoes`).
- Nova pasta `docs/`: relato da reorganização de novembro de 2026 (`reorganizacao-2026-11.md`), plano de ação com o
  status de cada fase (`plano-de-acao.md`) e a análise inicial do código (`analise-inicial-2026-11.md`), com um índice
  em `docs/README.md`. Até agora a análise e o plano existiam só fora do repositório.
- README: seção "Ferramentas utilizadas" (Visual Studio Code, GitHub Copilot e Claude Code), deixando claro que
  são ferramentas e não autoras.

---

## [1.5.0] - 2026-11-06

Fase 4 de [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17): reprodutibilidade. Os resultados
(vitórias, mortes, sobrevivências) são **idênticos** aos da v1.4.0 para os mesmos parâmetros e sementes.

### Adicionado
- `metadata.json` em cada run: versão, commit, branch, arquivos alterados não commitados, argumentos, parâmetros
  efetivos do agente genético, regra das sementes, Python, plataforma e versões das bibliotecas.
- `reproduzir.py <pasta>`: refaz um run a partir do `metadata.json`, avisa sobre diferenças de código ou ambiente e
  compara os resultados.
- Parâmetros do agente genético pela linha de comando: `--populacao`, `--geracoes`, `--cromossomo`, `--mutacao` e
  `--cruzamento`; e `--saida` para escolher a pasta do run ([#13]).
- `utils/versao.py` como fonte única da versão.
- `executar_benchmark(..., parametros_agentes=None)` nos 5 benchmarks; `main.rodar_benchmark(cli_args)`.
- `tests/test_reprodutibilidade.py` (13 testes).

### Desempenho
- **Agente genético de 15 a 25 vezes mais rápido** com resultados idênticos (padrão 100 × 500 × 100 em 4x4:
  17–22 s → cerca de 1 s). `World.clone()` deixou de usar `copy.deepcopy`, que respondia por ~73% do tempo; a seleção
  usa `Individual.copia()`; e o fitness é guardado em cache por cromossomo.

### Modificado
- `main.py`, `pygad/le_resultados.py` e `pygad/wumpus_AG_pygad.py` normalizados para finais de linha LF.

### Corrigido
- Os gráficos passam a usar sempre o backend `Agg` do matplotlib (`utils/graficos.py`, `benchmark_fast.py`,
  `benchmark_graficos.py`). Sem isso, o matplotlib tentava o Tk e falhava de forma intermitente em instalações do
  Python com Tk incompleto (no Windows, 4 de 5 rodadas da suíte de testes falhavam). O projeto só salva gráficos em
  arquivo, então nada muda nos resultados.

---

## [1.4.0] - 2026-11-06

Reorganização do repositório, testes e CI, e correção dos bugs #18 a #24 (Fases 1 a 3 de [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17)),
feitas na branch `reorg/v2`. Também foram criadas as tags retroativas `v1.1.0`, `v1.2.0` e `v1.3.0`.

> ⚠️ **As correções abaixo mudam os resultados dos experimentos.** Mundos, evolução do AG e fitness para cada
> semente não são mais os mesmos da v1.3.0. Os números do Release `v1.3.0-dados` e de `exemplos/` não são
> comparáveis com os desta versão.

### Corrigido
- **Agente lógico entrava em loop infinito** em todo mundo: a base de conhecimento não conhecia o tamanho do grid e
  "andava" para fora do mapa. Agora respeita o grid, usa a posição real do mundo e tem limite de `4 × N²` passos.
  É a primeira versão em que o benchmark padrão (`logico` + `genetico`) termina ([#18]).
- Fitness herdado do pai não é mais mantido depois da mutação ([#19]).
- O jogo termina na vitória ou na morte: o ouro não é pontuado várias vezes e nada acontece depois do fim ([#20]).
- O bônus de +25 do fitness passa a premiar matar o Wumpus; antes nunca era concedido ([#21]).
- Poços não caem mais na mesma casa; todo mundo tem exatamente `N // 2` poços ([#22]).
- `World` e o AG usam geradores aleatórios próprios; o AG usa a semente do mundo por padrão, então a mesma semente
  gera sempre o mesmo resultado, sem depender do `random` global ([#23]).
- Os 5 benchmarks seguem o mesmo contrato do `main.py --benchmark`; o CSV só tem colunas escalares e os dados extras
  vão para `dados_extra_<agente>_<N>x<N>.npz` ([#24]).

### Removido
- `logs/` (214 arquivos) e os 34 runs brutos de `exemplos/` (1.149 arquivos) saem do versionamento.
  Os dados completos foram preservados em `wumpus_dados_v1.3.0.zip`, publicado no Release `v1.3.0-dados`.

### Adicionado
- Testes automatizados em `tests/`: os 10 testes da branch `dev-melhorias` (adaptados à `main` e acelerados de 61 s
  para menos de 1 s) e `test_bugs_conhecidos.py`, que documentou os bugs #18 a #24 com `xfail` e hoje serve de
  teste de regressão (37 testes no total).
- README: seções "Regras deste Wumpus World" (diferenças em relação ao clássico e tabela do fitness) e
  "Os agentes não jogam nas mesmas condições".
- `LogicAgent(world, max_steps=None)`, `GeneticAgent(..., seed=None)` e `GeneticAlgorithm(..., seed=None)`.
- `LogicAgent.run()` devolve `{"history", "passos"}`.
- `pyproject.toml` com a configuração do pytest (timeout de 60 s, `xfail_strict`) e do ruff.
- CI no GitHub Actions: ruff e pytest em Ubuntu e Windows, Python 3.12 e 3.13.
- `requirements-dev.txt` com pytest, pytest-timeout e ruff.
- `__init__.py` em `agents/`, `ga/`, `utils/`, `world/` e `visual/`.
- `exemplos/README.md`: tabela com os parâmetros e as vitórias de cada um dos 34 exemplos.
- `exemplos/galeria/`: amostra de 12 gráficos do exemplo 33, com nomes curtos e sem acento.
- `CONTRIBUTING.md`: fluxo de branches, Conventional Commits, onde guardar resultados e regras de versão.
- `.mailmap`: unifica as identidades dos autores no histórico.

### Modificado
- `requirements.txt` com versões exatas. **Python mínimo passa a ser 3.12**, exigido pelo numpy 2.5.4 (antes: "3.8 ou superior", que as
  versões atuais de numpy e pandas não suportam).
- Removidos imports sem uso em `main.py`, `agents/genetic_agent.py` e `visual/visualizer.py` (sem mudança de comportamento).
- `.gitignore` passa a ignorar `logs/`, `results/`, pastas `run_*/`, `*.pkl` e os arquivos que os scripts gravam na raiz.
- `.gitattributes` marca imagens, zips e pickles como binários.
- Este CHANGELOG foi reescrito em português no formato Keep a Changelog, e as entradas antigas foram corrigidas (ver notas em cada versão).

---

## Pós-1.3.0 (sem tag, até `99e2eb4`, 2025-07-17)

Mudanças que entraram na `main` depois da 1.3.0 e não foram registradas na época.

### Adicionado
- 34 exemplos de varredura de parâmetros do agente genético em `exemplos/` (PR #12).
- Logs de execuções de benchmark com 4 a 14 de tamanho de mundo em `logs/`.

### Modificado
- **Parâmetros padrão do `GeneticAgent`** mudaram várias vezes sem registro (inclusive em commits com mensagem "fix typo" e "add exemplos"):

  | Commit | Data | População | Gerações | Cromossomo | Mutação | Cruzamento |
  |---|---|---:|---:|---:|---:|---:|
  | `64fbc06` | 10/07 | 50 | 100 | 20 | — | — |
  | `edfec71` | 13/07 | 50 | 1000 | 20 | — | — |
  | `8985b6a` | 14/07 | 100 | 1000 | 20 | — | — |
  | `4dd4390` | 14/07 | 100 | 500 | 100 | — | — |
  | `acb0536` | 14/07 | 100 | 500 | 100 | 0,02 | 0,9 |
  | `aaba31e` | 14/07 | 100 | 500 | 100 | 0,02 | 0,5 |
  | `18c3e7d` | 17/07 | 100 | 500 | 100 | 0,02 | 0,8 |

  Resultados gerados em datas diferentes podem ter usado parâmetros diferentes.

### Corrigido
- Chave `memory` renomeada para `memoria` no retorno do AG, para bater com `utils/graficos.py` (`aaba31e`).

---

## [1.3.0] - 2025-07-14

### Adicionado
- Captura automática da saída do terminal durante os benchmarks, salva em `terminal_output.txt` em cada execução.
- Context manager `capturar_saida_terminal()` para escrever no terminal e no arquivo ao mesmo tempo.
- Função `formatar_tempo()`, que mostra minutos para tempos a partir de 60 s.
- Menu interativo no `main.py` para escolher entre benchmark, agentes individuais e CLI customizada.
- Tratamento de erros durante as execuções dos agentes no `benchmark.py`.
- Gráficos avançados do agente genético gerados em subpastas `advanced_charts_genetico_NxN/`.
- Parâmetros `mutation_rate` e `crossover_rate` no `GeneticAgent` e no `GeneticAlgorithm`.
- Coleta de uso de memória, CPU e diversidade genética por geração.
- Implementação alternativa com PyGAD em `pygad/` (PR #4). Depende do módulo `WumpsimAG`, que **não está no repositório**.
- `requirements.txt`, incluindo `psutil`.

### Modificado
- Benchmarks executados dentro do context manager de captura de saída.
- Resumo dos resultados com percentuais e tempo formatado.
- Número padrão de execuções do benchmark no `main.py`: 32.

### Corrigido
- Restauração do `stdout` garantida mesmo em caso de erro.
- Validação dos dados extras antes de gerar os gráficos avançados.
- Gráficos de memória, CPU e diversidade.

> **Notas de correção (2026-11):** a versão original desta entrada dizia que `executar_benchmark()` passou a
> aceitar um logger opcional; isso não aconteceu (o logger é criado no `main.py`, mas não é repassado).
> Também dizia que havia "logs detalhados por agente"; os agentes recebem `logger = None` nos benchmarks.

---

## [1.2.0] - 2025-07-11

### Adicionado
- Resultados, logs e gráficos organizados por execução em `logs/run_AAAAMMDD_HHMMSS/`.
- Gráficos avançados: memória/CPU, evolução do fitness, convergência da população, violino, ECDF,
  mapa de calor, área empilhada e PCA (quando os dados estão disponíveis).
- Logger por agente, com arquivo por execução.
- Exportação de métricas em CSV para cada benchmark.
- Cabeçalhos explicativos nos arquivos principais.
- Parâmetros de benchmark pela linha de comando: número de execuções, tamanhos de mundo, agentes e modo silencioso.

### Modificado
- Funções de gráficos centralizadas em `utils/graficos.py`.
- Logger com `flush` imediato.

### Corrigido
- Sobrescrita de arquivos de log e de resultados.
- Imports e caminhos para funcionar em mais de um sistema operacional.

### Desempenho
- Execução paralela com `joblib` (somente em `benchmark_fast.py`).

---

## [1.1.0] - 2025-07-10

### Adicionado
- Visualização gráfica com `pygame` (`visual/visualizer.py`), mostrando vitória, morte e grito.
- Benchmark automático com mundos 4x4, 6x6 e 8x8.
- Execução paralela com `joblib.Parallel`.
- Gráficos comparativos gerados a partir do CSV.
- CLI com `argparse` no `benchmark_graficos.py`.
- Tutorial de execução (`tutorial_execucao.md`).

### Modificado
- `World.step()` dividido em `move_agent()` e `interact()`.
- Regras de inferência do agente lógico.
- Elitismo e mutação no agente genético.
- Validação das ações digitadas no agente manual.

### Corrigido
- `fitness = None` ao avaliar indivíduos.
- Mapeamento inválido na mutação do agente genético.

> **Notas de correção (2026-11):** a versão original citava os métodos `mover()` e `interagir()`
> (os nomes reais são `move_agent()` e `interact()`) e um arquivo `RELEASE_NOTES.md`, que nunca existiu.
> O `Visualizer` existe, mas não é chamado pelo `main.py`.

[Não lançado]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.8.0...main
[1.8.0]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.3.0
[1.2.0]: https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.2.0
[1.1.0]: https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.1.0
[#18]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/18
[#19]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/19
[#20]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/20
[#21]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/21
[#22]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/22
[#23]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/23
[#24]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/24
[#13]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/13
[#30]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/30
[#37]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/37
[#38]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/38
[#39]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/39
[#40]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/40
[#31]: https://github.com/ingrid-kiki/wumpus_world_modular/issues/31
