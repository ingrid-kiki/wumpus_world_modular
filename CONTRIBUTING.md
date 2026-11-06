# Como contribuir

## Branches

- A `main` só recebe mudanças por **Pull Request**, com pelo menos uma revisão.
- Crie uma branch curta por tarefa, a partir da `main` (ou da branch de integração em uso, como `reorg/v2`):

  | Prefixo | Uso | Exemplo |
  |---|---|---|
  | `feat/` | funcionalidade nova | `feat/visualizacao-cli` |
  | `fix/` | correção de bug | `fix/logic-agent-limites` |
  | `test/` | testes | `test/world-pocos` |
  | `docs/` | documentação | `docs/regras-do-jogo` |
  | `chore/` | manutenção, configuração, limpeza | `chore/requirements-pin` |

- Apague a branch depois do merge.
- Antes de abrir a PR, traga as mudanças mais recentes da branch de destino (`git pull --rebase origin main`).

## Commits

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/):

```
<tipo>(<escopo opcional>): <resumo no imperativo, em minúsculas>

<corpo opcional explicando o porquê>

Refs #<issue>
```

Exemplos:

```
fix(logic): impede a base de conhecimento de sair do grid
test(world): verifica que poços não se sobrepõem
docs: atualiza comandos do tutorial
```

Regras:

- **Um assunto por commit.** Evite mensagens como "melhorias" ou "fix typo" sem dizer o quê.
- **Nunca misture código e resultados de execução no mesmo commit.**
- Correção de bug vem acompanhada do teste que mostra o bug.

## Resultados de execução

As pastas `logs/`, `results/` e `run_*/` são ignoradas pelo git. Para compartilhar resultados:

1. Compacte a pasta do run (`logs/run_AAAAMMDD_HHMMSS/`).
2. Anexe o zip a um **GitHub Release** e descreva os parâmetros usados.
3. Se for só uma amostra para o README, coloque poucos gráficos em `exemplos/galeria/`, com nomes curtos e sem acento.

## Versões

O projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/) (`MAJOR.MINOR.PATCH`):

- **MAJOR**: muda comandos, caminhos ou o formato dos resultados.
- **MINOR**: funcionalidade nova compatível, ou correção que altera os números dos experimentos.
- **PATCH**: correção que não altera resultados.

Toda mudança visível entra na seção `[Não lançado]` do [CHANGELOG.md](CHANGELOG.md) na mesma PR.
Ao lançar uma versão, essa seção ganha número e data, e o commit recebe uma tag `vX.Y.Z`.
