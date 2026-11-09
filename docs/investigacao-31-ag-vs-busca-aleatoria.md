# Investigação: o agente genético supera a busca aleatória? (#31)

Experimentos de 09/11/2026 sobre o código da versão `1.7.0.dev0`. Para refazer:

```bash
python -m experimentos.comparar_metodos --fase confirmacao
```

```bash
python -m experimentos.comparar_metodos --fase hipoteses
```

## Como foi medido

- Todos os métodos recebem **o mesmo número de avaliações de fitness** e usam a mesma função de fitness.
- Cada cenário usa **100 mundos** (sementes 0 a 99). O resultado é a vitória ao executar a melhor sequência encontrada.
- A comparação é **pareada por mundo**, com o teste exato de McNemar e a correção de Holm para comparações múltiplas.
- "AG do projeto" é o `GeneticAlgorithm` atual com população 40, mutação 0,02 e cruzamento 0,8.
- Praticamente todos os mundos têm solução: só 1 dos 100 mundos 4x4 não tem caminho até o ouro; nos demais tamanhos, todos têm.

## Resultado 1: a busca aleatória vence mais em todos os cenários

Vitórias em 100 mundos (AG do projeto / busca aleatória), com 100 genes:

| Mundo | 500 avaliações | 2.000 avaliações | 10.000 avaliações |
|---|---|---|---|
| 4x4 | 85 / 98 | 89 / 99 | 95 / 99 |
| 6x6 | 90 / 99 | 92 / 100 | 94 / 100 |
| 8x8 | 84 / 95 | 85 / 100 | 88 / 100 |
| 10x10 | 69 / 95 | 73 / 100 | 77 / 100 |
| 14x14 | 62 / 74 | 68 / 89 | 68 / 99 |

Com 40 genes:

| Mundo | 500 avaliações | 2.000 avaliações | 10.000 avaliações |
|---|---|---|---|
| 4x4 | 90 / 97 | 92 / 99 | 93 / 99 |
| 6x6 | 83 / 98 | 88 / 100 | 91 / 100 |
| 8x8 | 66 / 81 | 70 / 94 | 74 / 99 |
| 10x10 | 43 / 65 | 46 / 79 | 51 / 95 |
| 14x14 | 33 / 41 | 36 / 54 | 36 / 71 |

A busca aleatória venceu mais nos **30 cenários**, com diferença significativa em **21** (p ajustado < 0,05). O AG não foi melhor em nenhum.

## Resultado 2: por que o AG perde

Vitórias em 100 mundos, com 2.000 avaliações:

| Método | 6x6, 40 genes | 6x6, 100 | 10x10, 40 | 10x10, 100 | 14x14, 40 | 14x14, 100 |
|---|---|---|---|---|---|---|
| **Busca aleatória** | **100** | **100** | **79** | **100** | **54** | **89** |
| AG do projeto | 88 | 92 | 46 | 73 | 36 | 68 |
| AG, população 20 | 85 | 86 | 42 | 69 | 30 | 58 |
| AG, população 100 | 96 | 97 | 54 | 85 | 40 | 69 |
| AG, torneio de 2 | 90 | 92 | 53 | 84 | 37 | 71 |
| AG, torneio de 3 | 86 | 93 | 51 | 79 | 35 | 67 |
| AG, mutação 0,1 | 95 | 97 | 67 | 86 | 43 | 74 |
| AG, torneio de 3 e mutação 0,1 | 98 | 99 | 65 | 88 | 46 | 78 |
| AG, fitness com proximidade | 97 | 94 | 93 | 96 | **88** | 89 |
| AG, torneio de 3 e proximidade | 98 | 98 | 87 | 95 | **91** | 90 |

| Hipótese da #31 | Avaliação |
|---|---|
| **Falta de gradiente no fitness até o ouro** | **É a principal causa encontrada.** Somar um bônus de proximidade ao ouro foi a única mudança que superou a busca aleatória com significância (14x14, 40 genes: 88 e 91 contra 54) |
| **Diversidade e pressão seletiva** | **Contribuem, mas não explicam tudo.** Mutação 0,1 reduz as avaliações repetidas de cerca de 30% para 5% e melhora o AG, sem alcançar a busca aleatória |
| **Parâmetros** | **Contribuem.** População maior ajuda; nenhuma combinação testada sem proximidade supera a referência |
| **Representação** | **Não testada isoladamente.** O AG piora muito com 40 genes em relação a 100, e a busca aleatória também |

**Interpretação:** sem um sinal de progresso, a pontuação é quase plana até o agente pegar o ouro, e o que diferencia as sequências é sobreviver. O AG concentra a busca em poucas sequências seguras; a busca aleatória continua amostrando o espaço inteiro e, com poucas ações necessárias, acaba encontrando o ouro.

## Limites destes resultados

- Foi testada **uma configuração-base** do AG. O padrão do projeto (100 × 500 × 100, 50.000 avaliações) não foi avaliado, e os orçamentos foram até 10.000.
- O AG roda uma vez por mundo, com a semente do mundo: a variação do próprio AG não foi medida separadamente.
- O bônus de proximidade usa a posição do ouro. O AG já simula o mundo real, mas isso amplia o que ele sabe, o que precisa constar na tese.
- Em cenários com busca aleatória perto de 100%, o problema é fácil demais para distinguir métodos.

## O que muda na interpretação

O AG do projeto, como está, **não demonstra ganho sobre uma busca sem inteligência** nos cenários testados. Os resultados de `exemplos/` e os gráficos não permitem concluir o contrário.
