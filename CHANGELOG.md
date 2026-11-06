# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/).
Veja as regras em [CONTRIBUTING.md](CONTRIBUTING.md).

## [Não lançado]

Próxima etapa: refatoração (Fase 5, v2.0.0), ver [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17).

### Corrigido
- **Erros nos benchmarks** ([#30]): os 5 benchmarks passam a tratar uma execução que falha do mesmo jeito. Ela não
  conta mais como vitória, morte ou sobrevivência (o `benchmark.py` contava como "sobreviveu" e o `benchmark_fast.py`
  descartava sem aviso), entra na nova coluna `erros`, e o benchmark continua com as demais execuções (os outros
  três paravam). Os dados extras vêm da primeira execução sem erro.
- `python benchmark.py` não testa mais o agente manual, que pedia ações pelo teclado e falhava 3 vezes sem ninguém
  digitando.
- `terminal_output.txt` passa a incluir o **stderr**: tracebacks e avisos das execuções ficam salvos na pasta do run.

### Modificado
- `resultados_benchmark.csv` ganha a coluna `erros`. O resumo impresso mostra os erros quando há, e os percentuais
  usam o total de execuções. `reproduzir.py` compara a coluna `erros` quando os dois CSVs a têm.
- `utils/execucao.py`: `executar_uma()` e `contar()`, usadas pelos 5 benchmarks.

### Documentação
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

[Não lançado]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/v1.5.0...main
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
