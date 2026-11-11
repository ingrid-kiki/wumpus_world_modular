# Sequência de um passo do agente lógico

Mostra o que acontece em uma volta do laço de `LogicAgent.run`. O laço se repete até o jogo terminar ou até atingir `max_steps`,
que por padrão é 4 vezes o número de casas do mundo.

```mermaid
sequenceDiagram
    participant A as LogicAgent
    participant M as World
    participant K as LogicKnowledgeBase

    A->>M: is_done()
    M-->>A: jogo ainda em andamento
    A->>M: perceive()
    M-->>A: percepção da casa atual
    A->>A: guarda em perception_history
    A->>A: decide(perception)
    A->>K: infer_action(perception)
    K->>K: update_knowledge(perception)
    alt sente BRILHO
        K-->>A: AGARRAR
    else sente FEDOR
        K-->>A: TIRO
    else há vizinha ainda não visitada
        K->>K: neighbors()
        K-->>A: movimento até ela
    else todas as vizinhas já visitadas
        K->>K: neighbors()
        K-->>A: movimento até a menos visitada
    end
    A->>M: step(action)
    M->>M: move_agent(action) e interact(action)
    M->>M: perceive()
    M-->>A: percepção e status
    A->>K: update_position(action, agent_pos)
```

## Regras de decisão

`LogicKnowledgeBase.infer_action` testa as regras nesta ordem e usa a primeira que valer:

| Ordem | Condição | Ação |
|---|---|---|
| 1 | Sente `BRILHO` | `AGARRAR` |
| 2 | Sente `FEDOR` | `TIRO` |
| 3 | Existe vizinha ainda não visitada | Move para a primeira, na ordem cima, baixo, esquerda, direita |
| 4 | Todas as vizinhas já foram visitadas | Move para a menos visitada |

## Observações

- A base marca cada casa como `seguro` ou não, mas `infer_action` não consulta essa marca. A `BRISA` não muda a decisão, então
  o agente pode andar para um poço.
- A posição na base vem de `World.agent_pos`, para um movimento bloqueado pela parede não desencontrar a base do mundo.
- A percepção devolvida por `step` não é usada: a próxima volta do laço chama `perceive` de novo.
