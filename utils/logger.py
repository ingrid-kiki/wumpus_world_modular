# ==============================
# utils/logger.py
# ==============================

import os
from datetime import datetime

class Logger:
    def __init__(self, agente_nome):
        # Gera um timestamp para identificar o log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Define o diretório onde os logs serão salvos
        log_dir = "logs"
        # Cria o diretório de logs caso não exista
        os.makedirs(log_dir, exist_ok=True)
        # Define o caminho completo do arquivo de log, incluindo o nome do agente e o timestamp
        self.filepath = os.path.join(log_dir, f"{agente_nome}_{timestamp}.log")
        # Abre o arquivo de log para escrita em modo texto e codificação UTF-8
        self.file = open(self.filepath, "w", encoding="utf-8")
    
    def write(self, msg):
        # Escreve a mensagem no terminal (opcional)
        print(msg)
        # Escreve a mensagem no arquivo de log, adicionando uma quebra de linha
        self.file.write(msg + "\n")
    
    def close(self):
        # Fecha o arquivo de log
        self.file.close()


