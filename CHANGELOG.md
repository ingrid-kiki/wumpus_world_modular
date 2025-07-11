# 📦 CHANGELOG - Wumpus World Modular

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