# ==============================
# agents/logic_agent.py
# ==============================
"""
# Este arquivo implementa o AgenteLogico, um agente inteligente para o Wumpus World
# baseado em lógica simbólica. O agente utiliza uma base de conhecimento lógica
# para decidir cada ação com regras simples a partir das percepções do ambiente, atualizando seu
# conhecimento a cada passo. O histórico dos passos é registrado para análise,
# e o agente pode ser usado nos benchmarks do projeto.
"""

from agents.agente import Agente
from agents.logic_knowledge_base import BaseConhecimento

PASSOS_POR_CASA = 4  # limite de passos: 4 vezes o número de casas do mundo (#18)


class AgenteLogico(Agente):
    def __init__(self, mundo, max_passos=None):
        super().__init__(mundo)
        # Base de conhecimento lógica para inferências; conhece o tamanho do grid (#18)
        self.conhecimento = BaseConhecimento(tamanho=mundo.tamanho)
        # Limite de passos: garante que executar() sempre termina (#18)
        self.max_passos = max_passos if max_passos is not None else PASSOS_POR_CASA * mundo.tamanho * mundo.tamanho

    def executar(self):
        """
        Executa o ciclo de vida do agente lógico.
        Atualiza a base de conhecimento e decide a próxima ação com regras simples.
        """
        passo = 1  # Contador de passos do agente
        # Continua enquanto o jogo não termina (vitória ou morte) e há passos disponíveis
        while not self.mundo.terminou() and passo <= self.max_passos:
            # Obtém percepções do ambiente na posição atual
            percepcao = self.mundo.perceber()

            # Exibe percepção atual
            print(f"[Passo {passo}] Percepção: {percepcao}")

            # Decide próxima ação com base na percepção
            acao = self.decidir_acao(percepcao)

            # Exibe ação escolhida
            print(f"[Passo {passo}] Ação decidida: {acao}")

            # Executa ação no mundo e registra o passo
            percepcao_depois, status = self.mundo.agir(acao)
            self.registrar_passo(acao, percepcao_depois, status)

            # Atualiza a posição na base de conhecimento com a posição real do mundo
            self.conhecimento.atualizar_posicao(acao, self.mundo.posicao_agente)

            # Exibe status do agente após a ação no terminal
            print(f"[Passo {passo}] Status do agente: {status}\n")
            passo += 1  # Incrementa o passo

        # Exibe o histórico completo ao final
        print("📝 Histórico:")
        for item in self.historico:
            print(f"Passo {item['passo']}: {item['acao']} -> {item['percepcao']}")

        return self.resultado()

    def decidir_acao(self, percepcao):
        """
        Aplica a lógica simbólica do agente baseada nas percepções recebidas.
        Retorna a próxima ação lógica a ser executada.
        """
        return self.conhecimento.inferir_acao(percepcao)
