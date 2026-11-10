# Como contribuir

## Branches

- A `main` só recebe mudanças por **Pull Request**, com pelo menos uma revisão.
- Crie uma branch curta por tarefa, a partir da `main`:

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
- Antes do commit, rode `ruff format .` e `ruff check .`: o CI recusa código fora do padrão.

### Checagem automática antes do commit

O `pre-commit` roda as checagens do `ruff` em cada commit. Basta instalar uma vez em cada clone:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

Se o `ruff` recusar o commit, corrija o que ele apontou. Quando ele só reformatar os arquivos, adicione-os de novo com
`git add` e repita o commit. Os testes não rodam nessa etapa: use `python -m pytest` antes de abrir a PR.

Ao atualizar o `ruff` em `requirements-dev.txt`, atualize também o `rev` em `.pre-commit-config.yaml`.

## Guia de estilo

As regras marcadas com **(CI)** são verificadas pelo `ruff`. As demais valem na revisão da PR.

### Nomes

- Variáveis e funções em `snake_case`, classes em `PascalCase`, constantes em `MAIUSCULAS`.
- Código novo usa nomes em português e sem abreviações obscuras: `taxa_mutacao`, não `tm`.
- Há nomes antigos em inglês, como `agent_pos` e `draw_world`. Não os renomeie junto com outra mudança: a padronização
  fica para a refatoração.
- Dê nome aos números com significado: `TAMANHO_MINIMO`, em vez de um `2` solto no código.

### Funções

- Cada função faz uma coisa só. Se o nome precisa de "e", provavelmente são duas.
- Procure ficar em até 30 linhas.
- **(CI)** Complexidade de no máximo 10 por função. Exceções levam `# noqa: C901` e o motivo no mesmo comentário.
- **(CI)** Linhas de até 120 caracteres.

### Docstrings

- Toda função pública e toda classe nova têm docstring, começando pelo que ela faz.
- Explique parâmetros e retorno quando o nome não bastar, como em `coletar_metadados`.
- Cada arquivo começa com um cabeçalho dizendo para que ele serve.

### Comentários

- Explique o **porquê**: a regra do jogo, a decisão do método, o motivo de um caminho menos óbvio.
- Em algoritmos, como o genético, um comentário curto por etapa ajuda quem está aprendendo a acompanhar.
- Não repita o que o código já diz, nem deixe código antigo comentado: o git guarda o histórico.
- Toda exceção do lint (`# noqa`) indica a regra e, quando ela não for óbvia, o motivo.

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

A versão fica num lugar só: `utils/versao.py`. Entre lançamentos ela tem o sufixo `.dev0` (ex.: `1.5.0.dev0`).
Para lançar:

1. Tire o `.dev0` em `utils/versao.py` e dê número e data à seção `[Não lançado]` do CHANGELOG.
2. Faça o merge na `main` e crie a tag `vX.Y.Z` no commit de merge, com um GitHub Release.
3. Volte a versão para a próxima `.dev0` num commit seguinte.

## Resultados de referência

`tests/test_referencia.py` compara os resultados atuais com `tests/referencia.json`: mundos gerados, sequências de
ações e regras do fitness. Se ele falhar sem que você quisesse mudar resultados, há uma regressão.

Se a mudança for intencional, regenere o arquivo e explique o motivo no commit e no CHANGELOG:

```bash
python -m tests.referencia
```

## Experimentos

Todo run grava `metadata.json`. Antes de usar um resultado num texto ou na tese:

- rode a partir de um commit sem alterações pendentes (o `metadata.json` registra se havia);
- confira com `python reproduzir.py logs/run_...` que ele se repete.
