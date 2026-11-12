# CLAUDE.md

Instruções para o Claude Code neste repositório. Responda em português do Brasil.

## O projeto

Simulação do Wumpus World com agentes manual, lógico, genético e de busca aleatória, usada numa tese. Estado atual e pendências:
[`docs/resumo-2026-11.md`](docs/resumo-2026-11.md), [`docs/plano-boas-praticas.md`](docs/plano-boas-praticas.md) e as issues abertas.
Como usar o programa: [`tutorial_execucao.md`](tutorial_execucao.md).

## Comandos

Python 3.12 ou superior, com o ambiente em `.venv`.

```bash
pip install -r requirements-dev.txt
pre-commit install
python -m pytest
ruff check .
ruff format .
python main.py
python reproduzir.py logs/run_AAAAMMDD_HHMMSS
python -m experimentos.comparar_metodos --fase confirmacao
```

## Regras

**Autoria**
- Nunca adicionar `Co-Authored-By` de IA nem "Generated with Claude Code" em commits, PRs, Releases ou comentários. Ferramentas de IA não são autoras.
- Commits da Ingrid usam `45125081+ingrid-kiki@users.noreply.github.com`. Nunca colocar e-mail pessoal em commits ou arquivos.

**Fluxo de trabalho** (detalhes em [`CONTRIBUTING.md`](CONTRIBUTING.md))
- A `main` só recebe mudanças por PR, a partir de branches curtas (`feat/`, `fix/`, `test/`, `docs/`, `chore/`). Merge sempre com merge commit, nunca squash.
- Cada merge, Release, comentário em issue ou outra ação pública precisa de aprovação naquele caso; aprovação anterior não vale para a próxima.
- Conferir o CI no commit mais recente da PR antes de mesclar.
- Antes de arquivar ou descartar código ou branch, analisar o que vale aproveitar e informar primeiro.
- A `main` é protegida no GitHub: exige PR e os 4 ambientes do CI aprovados, e bloqueia force-push.
- Reescrita de histórico e `push --force` na `main` dependem de acordo com a equipe (#17) e exigem suspender a proteção.

**Qualidade**
- Só fazer commit se `python -m pytest` passar, checando o código de saída; não encadear com `| tail`, que esconde a falha.
- Correção de bug vem com o teste que a prova, e o teste deve falhar no código anterior.
- Ao criar, renomear ou remover um teste, atualizar `docs/testes.md` na mesma PR.
- Documentar só o que foi executado de fato.
- Registrar mudanças visíveis na seção `[Não lançado]` do `CHANGELOG.md`, na mesma PR. A versão fica em `utils/versao.py`.

**Resultados e método**
- Não mudar os resultados dos experimentos sem decisão explícita. Mudanças de limpeza ou desempenho precisam dar resultados idênticos.
- Decisões sobre o método do agente genético, como fitness e parâmetros padrão, são das autoras: propor opções com recomendação, sem alterar antes.
- `logs/` e saídas de execução não vão para o git.
- Ao rodar experimentos, não trocar de branch na mesma pasta; usar `git worktree` para trabalhar em paralelo.

**Refatoração:** a Etapa 3 do plano de boas práticas foi antecipada em 11/11/2026 e vem antes da comparação final da tese.
Cada PR precisa manter os resultados idênticos (teste de referência e números do `logico_seguro`). Nomes em português, sem acentos
em identificadores, chaves, colunas e nomes de arquivos gerados; mensagens e documentação mantêm os acentos.

## Windows

Problemas comuns estão na seção 11 do tutorial. O principal: clonar com `git -c core.longpaths=true clone`.
No Git Bash, para texto com barra invertida, escreva o script num arquivo em vez de usar heredoc ou `printf`.
