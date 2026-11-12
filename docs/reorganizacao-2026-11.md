# Reorganização do projeto (novembro de 2026)

Relato do trabalho feito em 06/11/2026 sobre o estado de julho de 2025 (v1.3.0): o que foi encontrado, o que foi
decidido, o que mudou e o que ficou pendente. Para as mudanças versão a versão, veja o [CHANGELOG](../CHANGELOG.md).

- Análise de partida: [analise-inicial-2026-11.md](analise-inicial-2026-11.md)
- Plano e status das fases: [plano-de-acao.md](plano-de-acao.md)
- Decisões de equipe: [#17](https://github.com/ingrid-kiki/wumpus_world_modular/issues/17)

O trabalho foi conduzido por Ingrid Mendes, com aprovação de Alfa Marine para os merges, usando o Claude Code como
ferramenta de apoio (ver "Ferramentas utilizadas" no [README](../README.md)).

---

## 1. Ponto de partida

A análise do código e do histórico (`main` @ `99e2eb4`) mostrou dois grupos de problemas.

**Versionamento**
- 97% do repositório eram saídas de execução: 1.437 arquivos e cerca de 100 MB no `.git`, para cerca de 2.000 linhas
  de código.
- O clone quebrava no Windows por causa de caminhos longos dentro de `exemplos/`.
- Não havia tags, embora o CHANGELOG citasse v1.1.0 a v1.3.0; o CHANGELOG tinha menções que não batiam com o código.
- A branch `dev-melhorias` tinha testes e melhorias nunca mesclados.
- Os resultados não registravam o commit nem os parâmetros usados. Os parâmetros padrão do agente genético mudaram
  6 vezes em julho de 2025 sem registro.

**Código**
- O agente lógico entrava em loop infinito em todos os mundos (por isso nenhum log tinha resultados dele).
- O ouro podia ser pontuado várias vezes e as ações continuavam valendo depois da vitória.
- Poços podiam cair na mesma casa; `World(seed)` reiniciava o gerador aleatório global.
- 4 dos 5 benchmarks não funcionavam com `main.py --benchmark`.

---

## 2. O que foi feito

O trabalho seguiu o [plano de ação](plano-de-acao.md). As Fases 1 a 3 foram feitas numa branch de integração
(`reorg/v2`) e mescladas de uma vez; a Fase 4 seguiu em branch curta, como pede o [CONTRIBUTING](../CONTRIBUTING.md).

| Fase | Principais entregas | Versão |
|---|---|---|
| 0. Preparação | Clone íntegro, ambiente `.venv`, issue #17 com as decisões de equipe | — |
| 1. Repositório limpo | `logs/` e os runs brutos de `exemplos/` fora do git (dados no Release `v1.3.0-dados`); `exemplos/README.md` com a tabela dos 34 experimentos; `CONTRIBUTING.md`, `.mailmap`; CHANGELOG reescrito; tags retroativas `v1.1.0` a `v1.3.0` | v1.4.0 |
| 2. Testes e CI | Testes trazidos da `dev-melhorias`; testes que documentaram cada bug antes da correção; dependências com versão fixa; GitHub Actions (Ubuntu e Windows, Python 3.12 e 3.13) | v1.4.0 |
| 3. Bugs | #18 a #24 corrigidas, um commit por bug. O benchmark padrão (`logico` + `genetico`) passou a terminar | v1.4.0 |
| 4. Reprodutibilidade | `metadata.json` em cada execução; `reproduzir.py`; parâmetros do AG pela linha de comando (#13); AG de 15 a 25 vezes mais rápido com resultados idênticos | v1.5.0 |

Merges: PR #25 (v1.4.0), PRs #26 e #27 (v1.5.0); PRs #28, #32, #33, #34 e o lançamento seguinte (v1.6.0: correção da
#30, pasta `docs/`, ferramentas no README, tutorial reescrito).
Releases publicados: [`v1.3.0-dados`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.3.0-dados),
[`v1.4.0`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.4.0),
[`v1.5.0`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.5.0) e
[`v1.6.0`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.6.0).

> ⚠️ **Os resultados mudaram na v1.4.0.** Mundos, evolução do AG e fitness por semente não são os mesmos da v1.3.0.
> Os números do Release `v1.3.0-dados` e de `exemplos/` não são comparáveis com os atuais. Da v1.4.0 para a v1.5.0
> os resultados são idênticos.

---

## 3. Decisões tomadas

| Decisão | Quem | Onde |
|---|---|---|
| Trabalhar numa branch de integração e mesclar de uma vez | Ingrid | — |
| Bônus de +25 do fitness premia **matar o Wumpus** | Ingrid | #21 |
| Python mínimo 3.12 (exigido pelo numpy 2.5.4) | — | #17 |
| Tags retroativas: `v1.1.0` → `64fbc06`, `v1.2.0` → `11a8c7e`, `v1.3.0` → `53f9055` | Ingrid e Alfa | #17 |
| Mesclar as Fases 1 a 3 como v1.4.0 | Ingrid e Alfa (por telefone) | #17, PR #25 |
| Commits só com o e-mail noreply do GitHub | Ingrid | — |
| Ferramentas de IA **não** entram como coautoras; as usadas ficam registradas no README | Ingrid | PR #32 |
| A Fase 6 também retira o `Co-Authored-By: Claude` de 30 commits de 06/11/2026 | Ingrid | #17 |
| Arquivar a `dev-melhorias` (tag `archive/dev-melhorias`) e fechar a PR #8 | Ingrid | PR #8 |
| Manter por enquanto as branches já mescladas | Ingrid | — |

---

## 4. Issues analisadas

| Issue | Resultado da análise |
|---|---|
| #14 Compatibilidade dos benchmarks | **Fechada.** Os 5 benchmarks funcionam com `main.py`, reproduzem e dão números idênticos entre si |
| `dev-melhorias` / PR #8 | **Arquivada.** Os valores de memória e CPU de lá eram inventados (`np.random.uniform`) e nunca entraram na `main`, que mede com `psutil` desde `4dd4390` |
| #15 PyGAD e DEAP | **Aberta, com plano.** `pygad/` não roda: depende do módulo `WumpsimAG`, ausente do repositório e de qualquer fonte pública, e usa outro mundo (7 ações). Plano: agente PyGAD sobre o nosso `World`, depois DEAP |
| #16 Outras metaheurísticas | **Aberta, com plano.** Não havia código. Protótipo comparou busca aleatória, subida de encosta, recozimento e o AG |
| #29 (nova) | Gráficos avançados usam só a primeira execução; a ideia de juntar todas veio da `dev-melhorias` |
| #30 (nova) | Benchmarks tratavam erros de formas diferentes (`benchmark.py` contava falha como "sobreviveu"). **Corrigida na v1.6.0** (PR #34), incluindo gravar o stderr no log |
| #31 (nova) | **A busca aleatória vence igual ou mais que o AG** com o mesmo número de avaliações, em todos os cenários testados |

O achado da #31 é o mais importante para a tese: sem uma referência, a taxa de vitória do AG não demonstra que ele é
bom. É um protótipo (uma configuração do AG, 30 mundos, sem teste estatístico), ainda a ser confirmado.

---

## 5. Problemas encontrados durante o trabalho

Registrados para não se repetirem:

- **Python 3.11 no CI:** o primeiro CI falhou porque o numpy 2.5.4 exige 3.12; o mínimo foi ajustado.
- **Gravidade do bug #19 superestimada** na análise inicial: o melhor indivíduo já saía certo, porque o elite vencia o
  empate. A correção foi mantida.
- **`metadata.json`** registrava o primeiro arquivo alterado sem a primeira letra (`enchmark.py`), por um `.strip()`
  na saída do `git status`. Corrigido antes do merge.
- **Lentidão do AG introduzida pela correção do #23:** o mundo passou a carregar o próprio gerador aleatório, copiado
  a cada simulação. Resolvido na v1.5.0 (`World.clone()` sem `deepcopy`).
- **PR #27 aberta com testes falhando:** o comando usado escondia o código de saída do pytest. A causa era o matplotlib
  tentando abrir janela num Tk incompleto; corrigido com o backend `Agg` antes do merge. Desde então, commits só saem
  se o pytest passar.
- **Finais de linha:** três arquivos estavam com CRLF apesar do `.gitattributes`; normalizados num commit separado.

---

## 6. Continuação (09/11/2026)

Depois da v1.6.0, uma varredura do projeto abriu as issues #37 a #42. Na `main`, ainda sem versão lançada (`1.7.0.dev0`):

| Item | Resultado | PR |
|---|---|---|
| #37 | Uma falha nos gráficos não interrompe mais o benchmark nem perde os resultados | #43 |
| Seção "NÃO ALTERAR" do `main.py` | Resultados e log gravados a cada etapa; gráficos para qualquer agente com dados extras; o comentário virou testes | #44 |
| #38, #39 e #40 | Entradas validadas (o mundo de tamanho 1 travava), caminhos do Windows na opção 5 e traceback do `benchmark_fast` no log | #45 |

Em PRs abertas, aguardando merge, nesta ordem:

| PR | Conteúdo |
|---|---|
| #46 | Agente `aleatorio` (busca aleatória), `experimentos/comparar_metodos.py` e o relato da investigação |
| #47 | Opção `--proximidade P` no agente genético, desligada por padrão |

A investigação da #31 está em [investigacao-31-ag-vs-busca-aleatoria.md](investigacao-31-ag-vs-busca-aleatoria.md).
**Principal conclusão:** com o mesmo número de avaliações, a busca aleatória venceu mais que o AG do projeto nos 30 cenários
testados, inclusive no padrão de 50.000 avaliações em mundos grandes. O bônus de proximidade ao ouro, adotado como opção,
foi a única mudança que superou a busca aleatória com significância.

---

## 7. Continuação (09 a 12/11/2026)

Depois da v1.7.0, o trabalho seguiu o [plano de boas práticas](plano-boas-praticas.md), que tem a lista completa das PRs.

| Data | O que foi feito | PRs |
|---|---|---|
| 09/11 | v1.7.0: busca aleatória, `--proximidade` e a investigação da #31; `CLAUDE.md` com as regras do projeto | #46 a #50, #52 |
| 09 e 10/11 | Etapa 1: teste de referência, cobertura no CI, `ruff format`, regras de lint, `pre-commit` e guia de estilo | #53 a #57 |
| 09/11 | `main` protegida: exige PR e os 4 ambientes do CI, e bloqueia force-push e exclusão (registrado em 10/11) | #59 |
| 10 e 11/11 | Etapa 2: 8 diagramas em `docs/arquitetura/`, conferidos com execução real e no GitHub | #58, #60 a #65, #67 |
| 11/11 | Investigação do agente lógico e o agente `logico_seguro`; lista dos testes em `docs/testes.md` | #66, #68 |
| 11 e 12/11 | Análise dos 5 benchmarks, v1.8.0 e divisão da Etapa 3 em 10 PRs | #69 a #71 |
| 12/11 | Etapa 3, PRs A a F: constantes, classe base de agente, sem `Logger`, benchmark único, funções curtas e janela da partida | #72 a #78 |

Em toda a Etapa 3, o teste de referência, os números do `logico_seguro` e a comparação byte a byte dos gráficos provaram
que os resultados não mudaram. A única regeneração da referência (#73) foi de formato, com as 165 execuções conferidas antes.

**Problemas encontrados nesta parte:**

- **CI falhou por formatação de Markdown:** o `ruff format` também formata os blocos Python dentro dos `.md`. Desde então,
  o `ruff format --check` roda até em commits só de documentação.
- **Commit incompleto na #76:** um `git add` que recebeu arquivos já removidos falhou em silêncio, e o commit levou só as
  remoções. Corrigido com um segundo commit antes do merge; desde então o `git status` é conferido antes do push.
- **Entrada do CHANGELOG na seção errada:** depois da v1.8.0, uma entrada caiu na seção da versão lançada; foi movida para
  `[Não lançado]`.
- **Emojis na janela:** a fonte padrão do pygame mostrava os emojis como quadrados; as percepções passaram a ser escritas.

**Decisões desta parte:**

| Decisão | Quem | Onde |
|---|---|---|
| Proteger a `main` | Ingrid e Alfa (por telefone) | #59 |
| Manter o agente `logico` e criar o `logico_seguro`, com desempate pela posição | Ingrid | #66, #68 |
| Antecipar a Etapa 3, antes da comparação final da tese | Ingrid | #71 |
| Nomes em português, sem acentos em identificadores, chaves, colunas e arquivos | Ingrid | #71 |
| Um benchmark só, com `--paralelo` | Ingrid | #69, #76 |
| Retirar o `Logger` e os `.log` | Ingrid | #74 |
| Oferecer a janela por uma pergunta no menu, e não por `--vis` | Ingrid | #78 |
| Toda PR atualiza o histórico, o plano de boas práticas e o plano de ação | Ingrid | #79 |

---

## 8. Pendências (atualizado em 12/11/2026)

| Item | Onde |
|---|---|
| Etapa 3: PRs G a J (nomes e acentos, tipos, pacote e `.npz`) e lançamento da v2.0.0 | [plano de boas práticas](plano-boas-praticas.md), #42 |
| Comparação final para a tese: busca aleatória, AG original, AG com proximidade e `logico_seguro`, em orçamentos menores | #31 |
| Testar proximidade com mutação 0,1 e medir a variação do próprio AG (várias execuções por mundo) | #31 |
| Rodar de novo os experimentos da tese com o código da v2.0.0 | Fase 4.6 |
| Gráficos com os dados de todas as execuções, talvez a partir do `.npz` | #29, PR I |
| Agente PyGAD sobre o nosso `World`, depois DEAP; resposta da Alfa sobre o `WumpsimAG` | #15 |
| Outras metaheurísticas (recozimento, busca tabu, colônia de formigas) | #16 |
| Inconsistências no README, no CONTRIBUTING e na LICENSE | #41 |
| Etapas 4 (código comentado) e 5 (otimização) do plano de boas práticas | [plano de boas práticas](plano-boas-praticas.md) |
| Fase 6: reescrever o histórico (dados antigos, `Co-Authored-By` e e-mail pessoal) | #17, #42 |
| Instalar o gancho do `pre-commit` em cada clone (`pre-commit install`) | [CONTRIBUTING](../CONTRIBUTING.md) |
