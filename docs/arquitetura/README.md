# Arquitetura do projeto

Diagramas que explicam como o programa é organizado e como uma execução acontece. Eles fazem parte da Etapa 2 do
[plano de boas práticas](../plano-boas-praticas.md).

## Diagramas

| Diagrama | Arquivo | Situação |
|---|---|---|
| Caso de uso | `caso-de-uso.md` | A fazer |
| Fluxograma geral | `fluxo-geral.md` | A fazer |
| Diagrama de classes | `classes.md` | A fazer |
| Fluxograma do algoritmo genético | `fluxo-ag.md` | A fazer |
| Sequência de uma execução do algoritmo genético | `sequencia-ag.md` | A fazer |
| Sequência de um benchmark completo | `sequencia-benchmark.md` | A fazer |
| Sequência de um passo do agente lógico | `sequencia-agente-logico.md` | A fazer |
| Fluxo de dados | `fluxo-de-dados.md` | A fazer |

## Convenções

- Os diagramas usam [Mermaid](https://mermaid.js.org/), que o GitHub desenha direto e o git versiona como texto.
- Cada diagrama fica no seu arquivo, com uma frase dizendo o que ele mostra e o que ficou de fora.
- As explicações são em português. Nomes de classes, funções e arquivos ficam exatamente como no código.
- Os diagramas descrevem o código **como ele é hoje**, sem antecipar a refatoração.
- O Mermaid não tem um tipo próprio para caso de uso, então esse diagrama é feito com um fluxograma.

## Como manter

Mudou o que um diagrama mostra? Atualize o diagrama na mesma PR.

O diagrama de classes é conferido por `tests/test_diagramas.py`: o teste falha se o diagrama citar uma classe que não
existe, ou se o código tiver uma classe fora do diagrama. As pastas `tests/` e `pygad/` não entram nessa conferência. Os
demais diagramas dependem da revisão da PR.
