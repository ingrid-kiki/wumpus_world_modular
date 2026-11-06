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

Merges: PR #25 (v1.4.0), PRs #26 e #27 (v1.5.0), PR #32 (ferramentas no README).
Releases publicados: [`v1.3.0-dados`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.3.0-dados),
[`v1.4.0`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.4.0) e
[`v1.5.0`](https://github.com/ingrid-kiki/wumpus_world_modular/releases/tag/v1.5.0).

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
| Manter por enquanto as branches já mescladas e a PR #28 aberta | Ingrid | — |

---

## 4. Issues analisadas

| Issue | Resultado da análise |
|---|---|
| #14 Compatibilidade dos benchmarks | **Fechada.** Os 5 benchmarks funcionam com `main.py`, reproduzem e dão números idênticos entre si |
| `dev-melhorias` / PR #8 | **Arquivada.** Os valores de memória e CPU de lá eram inventados (`np.random.uniform`) e nunca entraram na `main`, que mede com `psutil` desde `4dd4390` |
| #15 PyGAD e DEAP | **Aberta, com plano.** `pygad/` não roda: depende do módulo `WumpsimAG`, ausente do repositório e de qualquer fonte pública, e usa outro mundo (7 ações). Plano: agente PyGAD sobre o nosso `World`, depois DEAP |
| #16 Outras metaheurísticas | **Aberta, com plano.** Não havia código. Protótipo comparou busca aleatória, subida de encosta, recozimento e o AG |
| #29 (nova) | Gráficos avançados usam só a primeira execução; a ideia de juntar todas veio da `dev-melhorias` |
| #30 (nova) | Benchmarks tratam erros de formas diferentes (`benchmark.py` conta falha como "sobreviveu"); gravar o stderr no log |
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

## 6. Pendências

| Item | Onde |
|---|---|
| Investigar por que o AG não supera a busca aleatória | #31 |
| Gráficos com os dados de todas as execuções | #29 |
| Padronizar o tratamento de erros nos benchmarks e gravar o stderr | #30 |
| Agente PyGAD sobre o nosso `World`, depois DEAP; resposta da Alfa sobre o `WumpsimAG` | #15 |
| Busca aleatória como referência e outras metaheurísticas | #16 |
| Fase 5: refatoração (pacote, classe base de agente, runner único, linha de comando nova) | v2.0.0 |
| Fase 6: reescrever o histórico (dados antigos e `Co-Authored-By`) | #17 |
| Proteger a `main` | #17 |
| Rodar de novo os experimentos da tese com o código atual | Fase 4.6 |
| PR #28 (versão `1.6.0.dev0`) | aberta |
