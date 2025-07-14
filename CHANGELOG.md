# 📦 CHANGELOG - Wumpus World Modular

## [v1.3.0] - 2025-07-14

### Adicionado
- Integração total dos gráficos avançados (`utils/advance_graphs.py`) ao fluxo dos benchmarks, incluindo debug detalhado e verificação de salvamento dos arquivos.
- Coleta robusta de dados extras (`dados_extra`) para agentes genéticos, permitindo geração de gráficos como PCA, área empilhada, heatmap, ECDF, violin plot, curva de convergência e uso de recursos.
- Prints de debug e asserts para garantir que os gráficos são realmente salvos no diretório correto.
- Função `executar_agente` adicionada ao `main.py` para integração dinâmica com benchmarks modulares.
- Redirecionamento de toda a saída do terminal para arquivos de log por execução, facilitando auditoria e análise posterior.
- Blocos `try/except` com traceback detalhado para facilitar a depuração de erros em chamadas de geração de gráficos.
- Compatibilidade automática para aceitar tanto inteiros quanto listas como argumento de tamanhos de mundo nos benchmarks.
- Teste de salvamento de gráfico simples ao final de `gerar_graficos_avancados` para depuração.

### Modificado
- Estrutura dos benchmarks (`bm_fast.py`, `bm_fasting.py`) revisada para garantir integração correta com os gráficos avançados e coleta de dados extras.
- Ajuste nos caminhos relativos e absolutos para garantir que todos os arquivos (logs, CSVs, gráficos) sejam salvos sempre na pasta correta, independente do diretório de execução.
- Robustez na coleta de dados extras: tratamento de listas de listas, conversão para `np.array` quando necessário, e checagem de formato antes de plotar.
- Função de benchmark agora aceita tanto listas quanto inteiros para tamanhos de mundo, evitando erros de iteração.
- Melhoria na documentação inline e prints de debug para facilitar o entendimento do fluxo de dados e geração de gráficos.

### Corrigido
- Correção de erro ao tentar iterar sobre inteiro em vez de lista nos tamanhos de mundo.
- Correção de erro de importação dinâmica e ausência da função `executar_agente` no `main.py`.
- Ajuste no tratamento de dados extras para evitar listas vazias ou formatos incompatíveis com os gráficos.
- Correção de possíveis erros silenciosos na geração de gráficos, agora reportados via assert e prints detalhados.

### Performance
- Pequenas otimizações na coleta e agregação de dados extras para benchmarks genéticos.
- Melhoria na robustez do paralelismo e na escrita de logs.

### Documentação
- Atualização do `README.md` e do tutorial para refletir a integração dos gráficos avançados e as novas opções de benchmark.
- Expansão dos comentários e cabeçalhos explicativos nos arquivos principais, especialmente nos módulos de benchmark e gráficos.

---

## [v1.2.0] - 2025-07-11

### Adicionado
- Organização automática de resultados, logs e gráficos em subpastas individuais por execução em `/logs/run_YYYYMMDD_HHMMSS/`
- Geração de gráficos avançados: uso de memória/CPU, evolução do fitness, convergência da população, violino, ECDF, mapas de calor, área empilhada e PCA (quando dados disponíveis)
- Logger customizado para cada agente, com logs salvos por execução e agente
- Coleta e exportação de métricas detalhadas em CSV para cada benchmark
- Cabeçalhos explicativos em todos os arquivos principais do projeto
- Novos exemplos e instruções detalhadas no `README.md` e `tutorial_execucao.md`
- Parâmetros customizáveis para benchmarks: número de execuções, tamanhos de mundo, seleção de agentes e modo silencioso

### Modificado
- Benchmarks agora salvam todos os resultados e gráficos em subpastas organizadas por execução
- Funções de geração de gráficos centralizadas em `utils/graficos.py`
- Logger atualizado para garantir logs organizados e flush imediato
- Estrutura dos benchmarks adaptada para integração fácil com coleta de dados extras e geração de gráficos avançados
- Melhor documentação inline e comentários para facilitar o entendimento do código

### Corrigido
- Correção de possíveis sobrescritas de arquivos de log e resultados
- Ajustes em imports e caminhos para garantir compatibilidade multiplataforma
- Pequenos bugs em coleta de métricas e geração de gráficos

### Performance
- Execução paralela otimizada nos benchmarks com `joblib`
- Redução do tempo de escrita de logs e geração de gráficos

### Documentação
- README.md atualizado com exemplos, estrutura do projeto e descrição dos gráficos avançados
- Tutorial de execução revisado e expandido com todos os novos recursos
- Cabeçalhos e comentários explicativos adicionados em todos os arquivos principais

---

## [v1.1.0] - 2025-07-10

### Added
- Visualização gráfica com `pygame`, incluindo feedback de status (vitória, morte, grito)
- Benchmark automático com múltiplos tamanhos de mundo (4x4, 6x6, 8x8)
- Execução paralela com `joblib.Parallel` no benchmark
- Geração de gráficos comparativos automáticos (CSV + visual)
- CLI robusta com `argparse` para `main.py` e `benchmark_graficos.py`
- Novo tutorial de execução com todas as possibilidades de uso

### Changed
- Separação de lógica no método `step()` para `mover()` e `interagir()` no mundo
- Regras de inferência do agente lógico refinadas
- Estrutura do agente genético aprimorada com elitismo e mutação adequada
- Validação de ações no agente manual com mensagens de erro claras

### Fixed
- Correção do bug de `fitness = None` ao avaliar indivíduos
- Corrigido mapeamento inválido na mutação do agente genético

### Performance
- Paralelismo leve via `joblib` para acelerar execuções
- Estimativa de tempo de execução com base em amostras de benchmark

### Documentation
- Atualização do `README.md` e `tutorial_execucao.md`
- Novo arquivo `RELEASE_NOTES.md` para histórico detalhado

---