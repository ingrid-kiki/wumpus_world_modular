# 📦 CHANGELOG - Wumpus World Modular

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