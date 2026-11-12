# ==============================
# tests/conftest.py
# ==============================
"""
# Configuração compartilhada dos testes.
#
# GA_RAPIDO: parâmetros pequenos para o AgenteGenetico. Os padrões do agente
# (100 indivíduos x 500 gerações x 100 ações) levam mais de 10 s por execução,
# o que deixaria a suíte lenta demais para rodar a cada PR.
"""

GA_RAPIDO = {
    "tamanho_populacao": 30,
    "geracoes": 20,
    "tamanho_cromossomo": 20,
}
