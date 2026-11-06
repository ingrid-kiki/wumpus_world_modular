# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/).
Veja as regras em [CONTRIBUTING.md](CONTRIBUTING.md).

## [Não lançado]

Trabalho em andamento na branch de integração `reorg/v2`, que será mesclada na `main` como **v2.0.0**.
Plano e decisões em [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17).

### Removido
- `logs/` (214 arquivos) e os 34 runs brutos de `exemplos/` (1.149 arquivos) saem do versionamento.
  Os dados completos foram preservados em `wumpus_dados_v1.3.0.zip`, publicado no Release `v1.3.0-dados`.

### Adicionado
- Testes automatizados em `tests/`: os 10 testes da branch `dev-melhorias` (adaptados à `main` e acelerados de 61 s
  para menos de 1 s) e `test_bugs_conhecidos.py`, com 11 testes `xfail` que documentam os bugs #18 a #24.
- `pyproject.toml` com a configuração do pytest (timeout de 60 s, `xfail_strict`) e do ruff.
- CI no GitHub Actions: ruff e pytest em Ubuntu e Windows, Python 3.11 e 3.13.
- `requirements-dev.txt` com pytest, pytest-timeout e ruff.
- `__init__.py` em `agents/`, `ga/`, `utils/`, `world/` e `visual/`.
- `exemplos/README.md`: tabela com os parâmetros e as vitórias de cada um dos 34 exemplos.
- `exemplos/galeria/`: amostra de 12 gráficos do exemplo 33, com nomes curtos e sem acento.
- `CONTRIBUTING.md`: fluxo de branches, Conventional Commits, onde guardar resultados e regras de versão.
- `.mailmap`: unifica as identidades dos autores no histórico.

### Modificado
- `requirements.txt` com versões exatas. **Python mínimo passa a ser 3.11** (antes: "3.8 ou superior", que as
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

[Não lançado]: https://github.com/ingrid-kiki/wumpus_world_modular/compare/main...reorg/v2
[1.3.0]: https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.3.0
[1.2.0]: https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.2.0
[1.1.0]: https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.1.0
