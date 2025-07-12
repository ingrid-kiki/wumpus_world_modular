# ==============================
# utils/logger.py
# ==============================
'''
# Este módulo fornece a classe Logger para o projeto Wumpus World.
# O Logger permite registrar mensagens de execução em arquivos de log organizados por agente e execução,
# facilitando o acompanhamento, depuração e análise dos experimentos realizados nos benchmarks.
# Os logs são salvos automaticamente nas pastas de saída de cada execução.
'''

import os
from datetime import datetime

class Logger:
    def __init__(self, agente_nome, output_dir=None):
        # Gera um timestamp para identificar o log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Usa o diretório de saída informado ou padrão 'logs'
        log_dir = output_dir if output_dir else "logs"
        os.makedirs(log_dir, exist_ok=True)
        # Define o caminho completo do arquivo de log
        self.filepath = os.path.join(log_dir, f"{agente_nome}_{timestamp}.log")
        self.file = open(self.filepath, "w", encoding="utf-8")
    
    def write(self, msg):
        print(msg)
        self.file.write(msg + "\n")
        self.file.flush()  # Garante escrita imediata
    
    def close(self):
        self.file.close()


