# Plano de ação faseado

Base: [analise-inicial-2026-11.md](analise-inicial-2026-11.md) (os números entre parênteses, como "bug 1", remetem às
seções 3 e 4 de lá). Decisões de equipe: [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17).
O relato do que foi feito está em [reorganizacao-2026-11.md](reorganizacao-2026-11.md).

## Status (atualizado em 09/11/2026, v1.6.0 lançada e `1.7.0.dev0` em andamento)

| Fase | Status | Onde |
|---|---|---|
| 0. Preparação | ✅ Concluída, exceto proteger a `main` (aguarda decisão na #17) | #17 |
| 1. Repositório limpo | ✅ Concluída | v1.4.0 (PR #25), Release `v1.3.0-dados`, tags `v1.1.0` a `v1.3.0` |
| 2. Testes e CI | ✅ Concluída | v1.4.0 (PR #25) |
| 3. Bugs críticos | ✅ Concluída: #18 a #24 | v1.4.0 (PR #25) |
| 4. Reprodutibilidade | ✅ Concluída, exceto rodar de novo os experimentos da tese (4.6) | v1.5.0 (PRs #26 e #27), #13 |
| 5. Refatoração | ⏳ Não iniciada | v2.0.0 |
| 6. Reescrever o histórico | ⏳ Aguarda acordo de todas; inclui retirar `Co-Authored-By` de 30 commits | #17 |

**O que mudou em relação ao plano original:**
- As Fases 1 a 3 foram feitas numa branch de integração (`reorg/v2`) e entraram na `main` juntas como **v1.4.0**,
  em vez de uma tag por fase (v1.3.1, v1.4.0 e v1.5.0 do plano). A Fase 4 virou a **v1.5.0**.
- O Python mínimo virou **3.12**, e não 3.11: o numpy 2.5.4 exige 3.12.
- A branch `dev-melhorias` foi arquivada na tag `archive/dev-melhorias` (PR #8 fechada); o que valia dela entrou na
  v1.4.0 ou foi registrado na #29.
- Pendências que surgiram das análises: #29 e #31 (ver o relato). A #30 foi corrigida na **v1.6.0**, uma versão de
  manutenção fora do plano original (correção de erros nos benchmarks, pasta `docs/`, tutorial reescrito).
- Depois da v1.6.0, entraram na `main` as correções #37 a #40 e o salvamento a cada etapa. A investigação da #31
  (busca aleatória contra o AG) e a opção `--proximidade` estão nas PRs #46 e #47. A próxima versão é a **v1.7.0**.

---

O texto abaixo é o plano como foi escrito em 06/11/2026, antes da execução.

Princípios:
- **Uma fase = uma ou mais PRs pequenas**, cada uma com um assunto só.
- **Código e dados nunca no mesmo commit.**
- **Toda correção de bug entra junto com o teste que a prova.**
- **Cada fase termina com uma tag**, para que qualquer resultado possa ser ligado a uma versão.

```
Fase 0 ─► Fase 1 ─► Fase 2 ─► Fase 3 ─► Fase 4 ─► Fase 5
preparo   repo      testes    bugs      reprodu-  refatoração
          limpo     + CI      críticos  tibilidade  (v2.0.0)
          v1.3.1    v1.4.0    v1.5.0    v1.6.0     v2.0.0
                                                   └► Fase 6 (opcional): reescrever histórico
```

---

## Fase 0 — Preparação (½ dia)

**Objetivo:** ter um ambiente de trabalho confiável antes de mexer em qualquer coisa.

| # | Tarefa | Observação |
|---|---|---|
| 0.1 | Clonar de novo o repositório com `git -c core.longpaths=true clone …` | A pasta `wumpus/` daqui é uma **cópia sem `.git`**: serve de referência, mas não dá para commitar a partir dela |
| 0.2 | Ativar `git config --global core.longpaths true` (e, se possível, *long paths* no Windows) | Evita o checkout quebrado visto na análise |
| 0.3 | Criar `.venv` e instalar o `requirements.txt`; anotar as versões instaladas (`pip freeze`) | Essas versões viram o primeiro *pin* na Fase 2 |
| 0.4 | Combinar com a equipe (Ingrid e Alfa): fluxo de PR, quem revisa, o que fazer com `dev-melhorias` e se o histórico poderá ser reescrito na Fase 6 | Decisões de equipe, não técnicas |
| 0.5 | Proteger a `main` no GitHub (merge só via PR) | |

**Pronto quando:** clone íntegro (`git fsck` sem erro), ambiente rodando `python main.py`, decisões de 0.4 registradas numa issue.

---

## Fase 1 — Limpeza do repositório e versionamento retroativo → `v1.3.1`

**Objetivo:** parar o crescimento do repo e dar nome às versões que já existem. Nenhuma linha de código Python muda.

| # | Tarefa | Resolve |
|---|---|---|
| 1.1 | Tags retroativas: `v1.1.0` (`64fbc06`/`46ef7fa`), `v1.2.0` (`11a8c7e`), `v1.3.0` (`53f9055`). Conferir o commit exato com a equipe antes | Sem tags |
| 1.2 | `.gitignore`: adicionar `logs/`, `results/`, `**/run_*/`, `*.pkl` | `.gitignore` incoerente |
| 1.3 | `git rm -r --cached logs/` e manter em `exemplos/` só 1–2 exemplos curados, com nomes curtos (`exemplos/ex01/`) e sem `terminal_output.txt` gigante | Repo 97% dados; caminhos longos |
| 1.4 | Publicar os runs completos como zip anexado a um **GitHub Release** `v1.3.0-dados` (ou Zenodo, se for citar na tese) e linkar no README | Dados preservados fora do git |
| 1.5 | `.gitattributes`: `*.png binary`, `*.pkl binary` | |
| 1.6 | `.mailmap` unificando "Alfa"/"Alfa Marine" e os dois e-mails da Ingrid | Identidades duplicadas |
| 1.7 | CHANGELOG: padronizar em português no formato *Keep a Changelog*, corrigir as menções falsas (`RELEASE_NOTES.md`, `mover()/interagir()`, logger opcional), registrar o que veio depois da v1.3.0 (PyGAD, exemplos) e abrir `[Unreleased]` | CHANGELOG impreciso |
| 1.8 | Adicionar `CONTRIBUTING.md` curto: nomes de branch (`feat/`, `fix/`, `docs/`, `chore/`), Conventional Commits, "apague a branch depois do merge" | Fluxo de branches e mensagens |

**Entregas:** PR `chore/limpeza-repo` (1.2–1.5), PR `docs/changelog-contributing` (1.6–1.8) e as tags.
**Pronto quando:** um clone novo no Windows funciona sem `longpaths`; o checkout tem menos de ~5 MB; `git tag` lista v1.1.0 a v1.3.1.

---

## Fase 2 — Rede de segurança: testes e CI → `v1.4.0`

**Objetivo:** conseguir provar que uma mudança não quebrou nada, antes de corrigir os bugs.

| # | Tarefa | Resolve |
|---|---|---|
| 2.1 | Decidir o destino de `dev-melhorias`: **trazer por cherry-pick** só os 9 testes e os `__init__.py`; deixar a reorganização de `benchmark/` para a Fase 5; arquivar a branch | Trabalho órfão |
| 2.2 | Adaptar os testes trazidos para a `main` atual e marcar com `@pytest.mark.xfail` os que falham por causa dos bugs conhecidos | |
| 2.3 | Escrever **testes de caracterização** para os bugs 1–6 (cada um em `xfail`, apontando a issue) | Bugs passam a ser visíveis |
| 2.4 | Limite de tempo nos testes (`pytest-timeout`), para o loop do agente lógico não travar o CI | Bug 1 |
| 2.5 | Fixar versões no `requirements.txt` (a partir da Fase 0.3) e separar `requirements-dev.txt` (pytest, ruff) | Dependências sem versão |
| 2.6 | GitHub Actions: `ruff check` + `pytest` em cada PR, rodando em Windows e Linux | Sem CI |
| 2.7 | Abrir uma issue por bug da análise (seção 3) e usar os números nas mensagens de commit (`fix: … (#14)`) | Rastreabilidade |

**Entregas:** PR `test/traz-testes-dev-melhorias`, PR `ci/github-actions`.
**Pronto quando:** CI verde na `main`, com os bugs conhecidos aparecendo como `xfail`.

---

## Fase 3 — Correção dos bugs críticos → `v1.5.0`

**Objetivo:** fazer os resultados do benchmark serem confiáveis. **Uma PR por bug**; cada PR tira o `xfail` do teste correspondente.

Ordem sugerida (do que mais distorce os resultados para o que menos distorce):

| # | PR | Mudança | Bug |
|---|---|---|---|
| 3.1 | `fix/world-rng-local` | `World` usa `self.rng = random.Random(seed)` em vez do `random.seed` global | 7 |
| 3.2 | `fix/world-pocos` | Poços sem sobreposição (incluir os já sorteados no `exclude`); `exclude=None` no lugar do default mutável | 6, 18 |
| 3.3 | `fix/world-fim-de-jogo` | Ouro coletável uma vez; nenhuma ação tem efeito depois de `GANHOU`/`MORTO`; `max_steps` no mundo | 3 |
| 3.4 | `fix/logic-agent-limites` | KB recebe o `size`, ignora vizinhos fora do grid e lê a posição real do mundo; o laço respeita `max_steps` | 1 |
| 3.5 | `fix/ga-fitness` | `fitness = None` ao mutar ou copiar; `break` em `GANHOU` no `evaluate`; remover ou corrigir o +25 do tiro | 2, 3, 4 |
| 3.6 | `fix/main-contrato-benchmark` | Os benchmarks alternativos passam a retornar o mesmo dict que o `benchmark.py`; `benchmark_fast` lê `dados_extra`; CSV só com colunas escalares (`dados_extra` vai para `.npz` separado) | 5, 15 |
| 3.7 | `docs/regras-do-jogo` | Documentar no README as regras deste Wumpus (flecha, tiro sem direção, vitória sem voltar para (0,0)) e a assimetria: o AG simula o mundo real, o agente lógico só vê percepções | 8, 9 |

⚠️ **Atenção para a tese:** depois desta fase, os números de vitória/morte **mudam**. Os resultados antigos (Release `v1.3.0-dados`) não são comparáveis com os novos; registrar isso no CHANGELOG e rodar os experimentos de novo.

**Pronto quando:** nenhum `xfail` sobrando dos bugs 1–7; o benchmark `logico + genetico` termina em 4x4, 6x6 e 8x8.

---

## Fase 4 — Reprodutibilidade dos experimentos → `v1.6.0`

**Objetivo:** qualquer gráfico ou CSV pode ser refeito a partir dos dados gravados com ele.

| # | Tarefa |
|---|---|
| 4.1 | Cada run grava `metadata.json`: commit, se havia mudanças não commitadas, versão do projeto, argumentos da CLI, parâmetros do AG, semente, versão do Python e das bibliotecas |
| 4.2 | Parâmetros do AG (`pop`, `gens`, `chrom`, `mut`, `cx`) passam a ser argumentos da CLI, em vez de defaults escondidos no código |
| 4.3 | `__version__` numa única fonte (pacote ou `pyproject.toml`), lido pelo `metadata.json` e pelo CHANGELOG |
| 4.4 | Cache de fitness no AG (o mundo é determinístico) e estimativa de tempo realista, ou remover a estimativa | Itens 10 e 11 da análise |
| 4.5 | Script `reproduzir.py <pasta_do_run>` que lê o `metadata.json` e roda de novo |
| 4.6 | Rodar os experimentos da tese de novo e publicar como Release `v1.6.0-dados` |

**Pronto quando:** reproduzir um run antigo gera os mesmos números (mesma semente → mesmo resultado).

---

## Fase 5 — Refatoração estrutural → `v2.0.0` (quebra de interface)

**Objetivo:** reduzir a duplicação e deixar o projeto fácil de estender. É *major* porque muda caminhos e comandos.

| # | Tarefa |
|---|---|
| 5.1 | Estrutura em pacote `wumpus/` (`world`, `agents`, `ga`, `bench`, `viz`, `constants`) com `pyproject.toml` |
| 5.2 | `constants.py` com ações, percepções e status (hoje duplicados em 4 arquivos) |
| 5.3 | Classe base `Agent` com `run(max_steps) -> Resultado` (dataclass) |
| 5.4 | Os 5 `benchmark_*.py` viram um runner só, com flags `--parallel`, `--silent` e `--out` (aproveitando a reorganização de `dev-melhorias`) |
| 5.5 | `main.py` com argparse de verdade: `main.py logico --size 4 --seed 42 --vis`; o menu interativo vira `--menu` |
| 5.6 | Ligar o `Visualizer` ao `--vis` (ou remover o pygame das dependências) |
| 5.7 | Renomear `pygad/` para `experimentos_pygad/` e incluir ou documentar a dependência `WumpsimAG`; ou mover para outra branch/repositório |
| 5.8 | Padronizar idioma dos identificadores e tirar acentos de chaves e nomes de arquivo (`vitorias`, `tempo_medio`, `grafico_vitorias.png`) |
| 5.9 | Atualizar README e tutorial com os comandos novos e uma seção "migrando da v1" |

**Pronto quando:** CI verde, README só com comandos que funcionam, nenhuma lista de ações ou de agentes duplicada.

---

## Fase 6 (opcional) — Reescrever o histórico

Só com acordo explícito de todos os colaboradores, depois da Fase 1 e com backup (`git clone --mirror`).

1. `git filter-repo --path logs --path exemplos --invert-paths` (preservando os exemplos curados).
2. `git push --force` e todos clonam de novo; forks e PRs abertas ficam inválidos.
3. Resultado esperado: `.git` de ~100 MB para menos de 1 MB.

Se não houver acordo, pular: a Fase 1 já impede o repositório de crescer.

---

## Resumo

| Fase | Versão | Esforço estimado | Muda resultados? | Risco |
|---|---|---|---|---|
| 0 Preparação | — | ½ dia | não | baixo |
| 1 Repo limpo | v1.3.1 | 1 dia | não | baixo |
| 2 Testes + CI | v1.4.0 | 1–2 dias | não | baixo |
| 3 Bugs críticos | v1.5.0 | 2–3 dias | **sim** | médio |
| 4 Reprodutibilidade | v1.6.0 | 1–2 dias | não (só metadados) | baixo |
| 5 Refatoração | v2.0.0 | 3–5 dias | não (se os testes passarem) | médio |
| 6 Histórico | — | ½ dia | não | **alto** (força push) |

As fases 1 e 2 podem andar em paralelo, por pessoas diferentes. A Fase 3 depende da 2. A Fase 5 depende da 3 e da 4.
