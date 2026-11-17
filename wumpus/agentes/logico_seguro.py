# ==============================
# wumpus/agentes/logico_seguro.py
# ==============================
"""
# Agente lógico que deduz quais casas são seguras antes de andar (agente "logico_seguro").
#
# Usa o mesmo laço do AgenteLogico, com outra regra de decisão: anda só por casas comprovadamente
# sem poço e, quando não há nenhuma nova para explorar, arrisca a casa menos suspeita, descartando
# as que certamente têm poço. É a regra D da investigação de 11/11/2026
# (docs/investigacao-agente-logico-2026-11.md). O agente "logico" continua com a regra original.
"""

from collections import deque
from collections.abc import Iterator

from wumpus.agentes.agente_logico import AgenteLogico
from wumpus.agentes.base_conhecimento import MOVIMENTOS, BaseConhecimento
from wumpus.mundo.constantes import AGARRAR, BRILHO, BRISA, FEDOR, TIRO, Percepcao, Posicao
from wumpus.mundo.mundo import Mundo


class BaseConhecimentoSegura(BaseConhecimento):
    """Base de conhecimento que deduz casas seguras e casas com poço certo a partir das brisas sentidas."""

    def vizinhas_de(self, pos: Posicao) -> Iterator[tuple[Posicao, str]]:
        """Vizinhas de `pos` dentro do grid, com a ação que leva até cada uma."""
        x, y = pos
        for dx, dy, acao in MOVIMENTOS:
            vizinha = (x + dx, y + dy)
            if self.dentro_do_mundo(vizinha):
                yield vizinha, acao

    def casas_seguras(self) -> set[Posicao]:
        """Casas visitadas e vizinhas de casa visitada sem BRISA: em nenhuma delas pode haver poço."""
        seguras = set(self.conhecidas)
        for pos, info in self.conhecidas.items():
            if BRISA not in info["percepcoes"]:
                seguras.update(vizinha for vizinha, _ in self.vizinhas_de(pos))
        return seguras

    def fronteira(self) -> set[Posicao]:
        """Casas ainda não visitadas que fazem divisa com alguma casa visitada."""
        return {
            vizinha for pos in self.conhecidas for vizinha, _ in self.vizinhas_de(pos) if vizinha not in self.conhecidas
        }

    def suspeita(self, casa: Posicao) -> int:
        """Quantas casas visitadas ao lado de `casa` sentiram BRISA: quanto maior, mais provável o poço."""
        return sum(
            BRISA in self.conhecidas[vizinha]["percepcoes"]
            for vizinha, _ in self.vizinhas_de(casa)
            if vizinha in self.conhecidas
        )

    def poco_certo(self, casa: Posicao, seguras: set[Posicao]) -> bool:
        """True se alguma casa com BRISA ao lado de `casa` não tem outra explicação para a brisa além dela."""
        for vizinha, _ in self.vizinhas_de(casa):
            info = self.conhecidas.get(vizinha)
            if info and BRISA in info["percepcoes"]:
                possiveis = [q for q, _ in self.vizinhas_de(vizinha) if q not in seguras]
                if possiveis == [casa]:
                    return True
        return False

    def primeiro_passo_ate(self, alvos: set[Posicao]) -> str | None:
        """Primeira ação do caminho mais curto até uma casa de `alvos`, andando só por casas visitadas."""
        fila: deque[tuple[Posicao, str | None]] = deque([(self.posicao_atual, None)])
        vistos = {self.posicao_atual}
        while fila:
            pos, primeira = fila.popleft()
            if pos in alvos and primeira:
                return primeira
            for vizinha, acao in self.vizinhas_de(pos):
                if vizinha not in vistos and (vizinha in self.conhecidas or vizinha in alvos):
                    vistos.add(vizinha)
                    fila.append((vizinha, primeira or acao))
        return None

    def arriscar(self, fronteira: set[Posicao], seguras: set[Posicao]) -> str | None:
        """Sem casa segura para explorar: vai à casa da fronteira menos suspeita que não tenha poço certo."""
        candidatas = sorted(
            (casa for casa in fronteira if not self.poco_certo(casa, seguras)),
            key=lambda casa: (self.suspeita(casa), casa),
        )
        for casa in candidatas:
            acao = self.primeiro_passo_ate({casa})
            if acao:
                return acao
        return None

    def permanecer(self) -> str:
        """Nada a explorar nem a arriscar: circula pelas casas conhecidas, preferindo a menos visitada."""
        visitadas = [
            (vizinha, acao) for vizinha, acao in self.vizinhas_de(self.posicao_atual) if vizinha in self.conhecidas
        ]
        if visitadas:
            return min(visitadas, key=lambda item: self.visitas.get(item[0], 0))[1]
        return AGARRAR  # longe do ouro, não muda nada no mundo: o agente fica parado

    def inferir_acao(self, percepcao: Percepcao) -> str:
        """Escolhe a ação: ouro, Wumpus, casa segura nova, a casa menos arriscada ou ficar em casas conhecidas."""
        self.atualizar_conhecimento(percepcao)
        if BRILHO in percepcao:
            return AGARRAR
        if FEDOR in percepcao:
            return TIRO  # o Wumpus está ao lado, então o tiro sempre acerta
        seguras = self.casas_seguras()
        fronteira = self.fronteira()
        return self.primeiro_passo_ate(fronteira & seguras) or self.arriscar(fronteira, seguras) or self.permanecer()


class AgenteLogicoSeguro(AgenteLogico):
    """AgenteLogico com a BaseConhecimentoSegura: o mesmo laço de percepção e ação, com decisão que evita poços."""

    def __init__(self, mundo: Mundo, max_passos: int | None = None) -> None:
        super().__init__(mundo, max_passos=max_passos)
        self.conhecimento = BaseConhecimentoSegura(tamanho=mundo.tamanho)
