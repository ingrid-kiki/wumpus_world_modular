# Sequência de um passo do agente lógico

Mostra o que acontece em uma volta do laço de `AgenteLogico.executar`. O laço se repete até o jogo terminar ou até atingir `max_passos`,
que por padrão é 4 vezes o número de casas do mundo.

```mermaid
sequenceDiagram
    participant A as AgenteLogico
    participant M as Mundo
    participant K as BaseConhecimento

    A->>M: terminou()
    M-->>A: jogo ainda em andamento
    A->>M: perceber()
    M-->>A: percepção da casa atual
    A->>A: decidir_acao(percepcao)
    A->>K: inferir_acao(percepcao)
    K->>K: atualizar_conhecimento(percepcao)
    alt sente BRILHO
        K-->>A: AGARRAR
    else sente FEDOR
        K-->>A: TIRO
    else há vizinha ainda não visitada
        K->>K: vizinhas_validas()
        K-->>A: movimento até ela
    else todas as vizinhas já visitadas
        K->>K: vizinhas_validas()
        K-->>A: movimento até a menos visitada
    end
    A->>M: agir(acao)
    M->>M: mover_agente(acao) e interagir(acao)
    M->>M: perceber()
    M-->>A: percepção e status
    A->>A: registrar_passo(acao, percepção, status)
    A->>K: atualizar_posicao(acao, posicao_agente)
```

## Regras de decisão

`BaseConhecimento.inferir_acao` testa as regras nesta ordem e usa a primeira que valer:

| Ordem | Condição | Ação |
|---|---|---|
| 1 | Sente `BRILHO` | `AGARRAR` |
| 2 | Sente `FEDOR` | `TIRO` |
| 3 | Existe vizinha ainda não visitada | Move para a primeira, na ordem cima, baixo, esquerda, direita |
| 4 | Todas as vizinhas já foram visitadas | Move para a menos visitada |

## Observações

- A base marca cada casa como `seguro` ou não, mas `inferir_acao` não consulta essa marca. A `BRISA` não muda a decisão, então
  o agente pode andar para um poço.
- A posição na base vem de `Mundo.posicao_agente`, para um movimento bloqueado pela parede não desencontrar a base do mundo.
- A percepção devolvida por `agir` não é usada: a próxima volta do laço chama `perceber` de novo.

## Agente `logico_seguro`

`AgenteLogicoSeguro` usa este mesmo laço. Só muda `inferir_acao`, em `BaseConhecimentoSegura`. Para ela, uma casa é segura se
foi visitada ou se é vizinha de casa visitada sem `BRISA`.

| Ordem | Condição | Ação |
|---|---|---|
| 1 | Sente `BRILHO` | `AGARRAR` |
| 2 | Sente `FEDOR` | `TIRO` |
| 3 | Existe casa segura ainda não visitada | Anda até a mais próxima, passando só por casas visitadas |
| 4 | Nenhuma casa segura nova | Vai à casa da fronteira menos suspeita, descartando as que certamente têm poço; no empate, a de menor linha e coluna |
| 5 | Nada a explorar nem a arriscar | Circula pelas casas conhecidas, preferindo a menos visitada |

Os motivos e as medições estão na [investigação de 11/11/2026](../investigacao-agente-logico-2026-11.md).
