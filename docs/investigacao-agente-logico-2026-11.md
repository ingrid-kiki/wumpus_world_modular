# Investigação do agente lógico (novembro de 2026)

Relato de 11/11/2026. Os números vêm de protótipos executados fora do programa: o código do projeto não foi alterado por esta
investigação.

## 1. Como o problema apareceu

Ao desenhar a sequência de um passo do agente lógico (`docs/arquitetura/sequencia-agente-logico.md`, Etapa 2 do
[plano de boas práticas](plano-boas-praticas.md)), notamos que a base de conhecimento marca cada casa como `seguro` ou não, mas a
decisão nunca consulta essa marca.

## 2. O que o código faz hoje

`LogicKnowledgeBase.infer_action` usa a primeira regra que valer:

| Ordem | Condição | Ação |
|---|---|---|
| 1 | Sente `BRILHO` | `AGARRAR` |
| 2 | Sente `FEDOR` | `TIRO` |
| 3 | Existe vizinha não visitada | Move para a primeira, na ordem cima, baixo, esquerda, direita |
| 4 | Todas as vizinhas já foram visitadas | Move para a menos visitada |

Consequências:

- `BRISA` não muda a decisão, então o agente pode andar para um poço.
- `update_knowledge` calcula `seguro`, mas `infer_action` não usa esse valor.
- Os comentários de `agents/logic_agent.py` e `agents/logic_knowledge_base.py` falam em "inferir ações seguras", o que não
  corresponde ao comportamento. O README é mais fiel: "lógica simbólica simples (regras IF/ELSE)".

## 3. Medição

Quatro formas de decidir foram comparadas com 1000 mundos por tamanho, sementes 0 a 999, os mesmos mundos para todas. O programa
estava no commit `b7848df`, e o Python era o 3.13.2. O script está na seção 7. Não houve teste estatístico.

| Forma | Regra |
|---|---|
| **A. Atual** | As regras da seção 2 |
| **B. Mínima** | Com `BRISA` na casa atual, prefere voltar por casa já visitada; se não houver, segue a regra atual |
| **C. Com memória, sem arriscar** | Uma casa só é segura se foi visitada ou é vizinha de casa visitada sem `BRISA`. Vai à casa segura não visitada mais próxima; sem nenhuma, permanece em casas conhecidas |
| **D. Com memória, arriscando** | Como C, mas sem casa segura escolhe a casa de fronteira menos suspeita, descartando as que certamente têm poço |

Em todas, as regras de `BRILHO` e `FEDOR` continuam em primeiro lugar.

**4x4** (987 mundos têm caminho até o ouro sem pisar em poço)

| Forma | Vitórias | Mortes | Sobreviveu sem vencer |
|---|---|---|---|
| A. Atual | 33,3% | 66,7% | 0,0% |
| B. Mínima | 58,2% | 15,7% | 26,1% |
| C. Com memória, sem arriscar | 52,3% | 0,0% | 47,7% |
| D. Com memória, arriscando | 80,5% | 19,3% | 0,2% |

**6x6** (994 mundos com caminho)

| Forma | Vitórias | Mortes | Sobreviveu sem vencer |
|---|---|---|---|
| A. Atual | 24,2% | 75,8% | 0,0% |
| B. Mínima | 66,8% | 8,5% | 24,7% |
| C. Com memória, sem arriscar | 61,0% | 0,0% | 39,0% |
| D. Com memória, arriscando | 87,3% | 12,7% | 0,0% |

**8x8** (996 mundos com caminho)

| Forma | Vitórias | Mortes | Sobreviveu sem vencer |
|---|---|---|---|
| A. Atual | 19,4% | 80,6% | 0,0% |
| B. Mínima | 77,1% | 5,8% | 17,1% |
| C. Com memória, sem arriscar | 73,5% | 0,0% | 26,5% |
| D. Com memória, arriscando | 90,9% | 9,1% | 0,0% |

## 4. O que os números mostram

- Todas as mortes, em todas as formas, foram por poço. Nenhuma foi pelo Wumpus: sentir `FEDOR` faz o agente atirar, e o tiro sempre
  acerta quem está ao lado.
- A forma atual piora quando o mundo cresce, de 33,3% para 19,4% de vitórias, enquanto as outras melhoram.
- A forma C nunca morreu, o que confirma que sua regra de segurança é correta para esses mundos, mas ela desiste em parte deles.
- A forma D teve a maior taxa de vitórias nos três tamanhos.

## 5. Opções consideradas

| Opção | Resultado dos experimentos | Esforço estimado | Observação |
|---|---|---|---|
| 1. Só documentar | Não muda | cerca de 30 min | O agente segue como referência fraca |
| 2. Manter `logico` e criar um agente novo com a regra D | `logico` não muda | 2 a 3 h com testes | Permite comparar o agente reativo com o que infere |
| 3. Substituir `logico` pela regra D | Muda todos os números do agente lógico | Exige rodar de novo os experimentos | Atualiza o teste de referência; versão MINOR |
| 4. Substituir `logico` pela regra B | Muda todos os números do agente lógico | cerca de 1 h, mais os novos experimentos | Ainda não é inferência, porque só olha a casa atual |

## 6. Decisão e pendências

**Decidido em 11/11/2026:** criar um agente novo, mantendo o `logico` como está (opção 2).

Também decidido em 11/11/2026:

1. A regra do agente novo é a D.
2. O nome do agente é `logico_seguro`.
3. Ele entra na comparação final da tese ([#31](https://github.com/ingrid-kiki/wumpus_world_modular/issues/31)). Com ele, a
   comparação com o algoritmo genético pode mudar, o que ainda precisa ser medido.
4. No empate entre casas igualmente suspeitas, vence a de menor linha e, depois, de menor coluna (seção 8).
5. Os comentários do agente atual que falavam em "inferir ações seguras" foram corrigidos.

## 7. Como repetir a medição

Salve o script abaixo num arquivo fora do projeto e rode, a partir da raiz do repositório:

```bash
python variantes_logico.py . 1000
```

<details>
<summary>Script usado na medição</summary>

```python
"""Compara, fora do projeto, variantes da decisão do agente lógico nos mesmos mundos."""

import contextlib
import io
import sys
import time
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from agents.logic_agent import LogicAgent  # noqa: E402
from agents.logic_knowledge_base import MOVIMENTOS, LogicKnowledgeBase  # noqa: E402
from experimentos.comparar_metodos import resolvivel  # noqa: E402
from world.world import World  # noqa: E402

N_MUNDOS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000


class Minima(LogicKnowledgeBase):
    """Com BRISA na casa atual, prefere voltar por casa já visitada."""

    def infer_action(self, perception):
        self.update_knowledge(perception)
        if "BRILHO" in perception:
            return "AGARRAR"
        if "FEDOR" in perception:
            return "TIRO"
        vizinhas = list(self.neighbors())
        livres = [(p, a) for p, a in vizinhas if p not in self.known]
        visitadas = [(p, a) for p, a in vizinhas if p in self.known]
        if "BRISA" in perception and visitadas:
            return min(visitadas, key=lambda i: self.visits.get(i[0], 0))[1]
        if livres:
            return livres[0][1]
        return min(vizinhas, key=lambda i: self.visits.get(i[0], 0))[1]


class ComMemoria(LogicKnowledgeBase):
    """Só entra em casa comprovadamente sem poço; sem nenhuma, não arrisca (opcionalmente arrisca a menos suspeita)."""

    arriscar = False

    def _vizinhas(self, pos):
        x, y = pos
        for dx, dy, acao in MOVIMENTOS:
            p = (x + dx, y + dy)
            if self.in_grid(p):
                yield p, acao

    def _seguras(self):
        seguras = set(self.known)
        for pos, info in self.known.items():
            if "BRISA" not in info["percepções"]:
                seguras.update(p for p, _ in self._vizinhas(pos))
        return seguras

    def _caminho_ate(self, alvos, permitidas):
        fila, vistos = deque([(self.current_pos, None)]), {self.current_pos}
        while fila:
            pos, primeira = fila.popleft()
            if pos in alvos and primeira:
                return primeira
            for p, acao in self._vizinhas(pos):
                if p not in vistos and (p in permitidas or p in alvos):
                    vistos.add(p)
                    fila.append((p, primeira or acao))
        return None

    def _fronteira(self):
        return {p for pos in self.known for p, _ in self._vizinhas(pos) if p not in self.known}

    def _suspeita(self, cand):
        return sum("BRISA" in self.known[p]["percepções"] for p, _ in self._vizinhas(cand) if p in self.known)

    def _poco_certo(self, cand):
        for p, _ in self._vizinhas(cand):
            info = self.known.get(p)
            if info and "BRISA" in info["percepções"]:
                seguras = self._seguras()
                desconhecidas = [q for q, _ in self._vizinhas(p) if q not in seguras]
                if desconhecidas == [cand]:
                    return True
        return False

    def infer_action(self, perception):
        self.update_knowledge(perception)
        if "BRILHO" in perception:
            return "AGARRAR"
        if "FEDOR" in perception:
            return "TIRO"
        seguras = self._seguras()
        fronteira = self._fronteira()
        acao = self._caminho_ate(fronteira & seguras, set(self.known))
        if acao:
            return acao
        if self.arriscar:
            candidatas = sorted((c for c in fronteira if not self._poco_certo(c)), key=self._suspeita)
            for c in candidatas:
                acao = self._caminho_ate({c}, set(self.known))
                if acao:
                    return acao
        # Sem casa segura para explorar: permanece em casas conhecidas
        vizinhas = [(p, a) for p, a in self._vizinhas(self.current_pos) if p in self.known]
        if vizinhas:
            return min(vizinhas, key=lambda i: self.visits.get(i[0], 0))[1]
        return "AGARRAR"  # sem saída segura na casa inicial: ação sem deslocamento


class ComMemoriaArriscando(ComMemoria):
    arriscar = True


VARIANTES = [
    ("A atual", LogicKnowledgeBase),
    ("B mínima (BRISA: volta)", Minima),
    ("C memória, sem arriscar", ComMemoria),
    ("D memória, arrisca", ComMemoriaArriscando),
]

print(f"{N_MUNDOS} mundos por tamanho, sementes 0 a {N_MUNDOS - 1}")
for tam in (4, 6, 8):
    resolv = sum(resolvivel(World(size=tam, seed=s)) for s in range(N_MUNDOS))
    print(f"\n{tam}x{tam}: {resolv} mundos resolvíveis ({resolv / N_MUNDOS:.0%})")
    for nome, classe in VARIANTES:
        v, m, s_, poco, wumpus, t0 = 0, 0, 0, 0, 0, time.perf_counter()
        for seed in range(N_MUNDOS):
            w = World(size=tam, seed=seed)
            a = LogicAgent(w)
            a.knowledge = classe(size=tam)
            with contextlib.redirect_stdout(io.StringIO()):
                a.run()
            if w.won:
                v += 1
            elif not w.is_alive:
                m += 1
                poco += w.agent_pos in w.pits
                wumpus += w.agent_pos == w.wumpus_pos
            else:
                s_ += 1
        print(
            f"  {nome:26s} vitórias {v / N_MUNDOS:6.1%} | mortes {m / N_MUNDOS:6.1%} (poço {poco}, Wumpus {wumpus}) "
            f"| sobreviveu {s_ / N_MUNDOS:6.1%} | {time.perf_counter() - t0:.1f}s"
        )
```

</details>

## 8. Implementação

O agente foi implementado em `agents/logico_seguro.py` (classes `AgenteLogicoSeguro` e `BaseConhecimentoSegura`) e pode ser usado
com `--agentes logico_seguro`.

A regra D do protótipo não dizia o que fazer quando duas casas da fronteira são igualmente suspeitas. No protótipo, o empate
dependia da ordem interna de um conjunto do Python, que não é garantida entre versões. Na implementação, vence a casa de menor
linha e, depois, de menor coluna. Assim o resultado é o mesmo em qualquer versão, e a regra fica fácil de descrever.

Com esse desempate, nos mesmos 1000 mundos por tamanho:

| Tamanho | Vitórias | Mortes | Sobreviveu sem vencer |
|---|---|---|---|
| 4x4 | 83,4% | 16,4% | 0,2% |
| 6x6 | 86,4% | 13,6% | 0,0% |
| 8x8 | 91,9% | 8,1% | 0,0% |

Em relação ao protótipo, as vitórias variam de −0,9 a +2,9 pontos percentuais. Esses números são conferidos por
`tests/test_logico_seguro.py`: uma mudança no comportamento do agente faz o teste falhar.
