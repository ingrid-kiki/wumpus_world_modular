# ==============================
# tests/conftest.py
# ==============================
'''
# Configuração compartilhada dos testes.
#
# GA_RAPIDO: parâmetros pequenos para o GeneticAgent. Os padrões do agente
# (100 indivíduos x 500 gerações x 100 ações) levam mais de 10 s por execução,
# o que deixaria a suíte lenta demais para rodar a cada PR.
'''

GA_RAPIDO = {
    "population_size": 30,
    "gens": 20,
    "chrom_length": 20,
}
