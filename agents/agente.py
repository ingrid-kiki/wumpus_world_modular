# ==============================
# agents/agente.py
# ==============================
"""
# Classe base de todos os agentes. Define o contrato que o programa espera de um agente:
#
# - o construtor recebe o mundo (Mundo) como primeiro argumento;
# - executar() joga uma partida e devolve o resultado no formato único:
#     {"historico": [...], "passos": N, "dados_extra": {...}, ...campos próprios do agente}
#
# Cada item do histórico descreve um passo já executado:
#     {"passo": 1, "acao": "DIREITA", "percepcao": ["BRISA"], "status": "OK", "posicao": [0, 1]}
# com a percepção e a posição depois da ação. "dados_extra" alimenta os gráficos avançados e fica
# vazio para os agentes que não têm esses dados.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from world.constantes import FIM_DE_JOGO, Percepcao
from world.world import Mundo

# Um passo do histórico: passo, acao, percepcao, status e posicao
Passo = dict[str, Any]
# O que executar() devolve: historico, passos, dados_extra e campos próprios de cada agente
Resultado = dict[str, Any]


class Agente(ABC):
    """Contrato comum dos agentes: recebem o mundo e devolvem o resultado de executar() no formato único."""

    def __init__(self, mundo: Mundo) -> None:
        self.mundo = mundo
        self.historico: list[Passo] = []

    @abstractmethod
    def executar(self) -> Resultado:
        """Joga uma partida no mundo e devolve self.resultado(...)."""

    def registrar_passo(self, acao: str, percepcao: Percepcao, status: str) -> None:
        """Acrescenta ao histórico um passo já executado, com a posição do agente depois da ação."""
        self.historico.append(
            {
                "passo": len(self.historico) + 1,
                "acao": acao,
                "percepcao": list(percepcao),
                "status": status,
                "posicao": list(self.mundo.posicao_agente),
            }
        )

    def executar_sequencia(self, acoes: Iterable[str], mostrar: bool = False) -> None:
        """Executa as ações no mundo real, na ordem, até o fim da sequência ou do jogo."""
        for acao in acoes:
            percepcao, status = self.mundo.agir(acao)
            self.registrar_passo(acao, percepcao, status)
            if mostrar:
                passo = len(self.historico)
                print(f"[Passo {passo}] Ação: {acao}")
                print(f"[Passo {passo}] Percepção recebida: {percepcao}")
                print(f"[Passo {passo}] Status do agente: {status}\n")
            if status in FIM_DE_JOGO:
                break

    def resultado(self, dados_extra: dict[str, Any] | None = None, **extras: Any) -> Resultado:
        """Resultado no formato único; `extras` acrescenta campos próprios do agente."""
        return {"historico": self.historico, "passos": len(self.historico), "dados_extra": dados_extra or {}, **extras}
