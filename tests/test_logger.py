# ==============================
# tests/test_logger.py
# ==============================
'''
# Este arquivo contém testes unitários para a classe Logger do projeto Wumpus World.
# O objetivo é garantir que o Logger cria corretamente arquivos de log e registra mensagens.
#
# Explicação do teste:
# - Cria um diretório temporário usando o recurso tmp_path do pytest.
# - Instancia o Logger, passando o nome do agente e o diretório temporário.
# - Escreve uma mensagem de teste no log.
# - Fecha o Logger para garantir que o arquivo seja salvo.
# - Procura no diretório temporário por arquivos de log criados com o padrão esperado.
# - Verifica se pelo menos um arquivo de log foi criado.
# - Abre o arquivo de log e verifica se a mensagem escrita está presente no conteúdo.
#
# Esse teste assegura que o Logger está funcionando corretamente para registrar logs de execução.
'''

import pytest
from utils.logger import Logger
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(BASE_DIR, "logs", f"run_{timestamp}")

def test_logger_creation(tmp_path):
    # Cria o Logger no diretório temporário com o nome "testagent"
    logger = Logger("testagent", output_dir=str(tmp_path))
    # Escreve uma mensagem de teste no log
    logger.write("Test log entry")
    # Fecha o Logger para garantir que o arquivo seja salvo
    logger.close()
    # Procura o arquivo criado no diretório temporário
    files = list(tmp_path.glob("testagent_*.log"))
    # Verifica se algum arquivo de log foi criado
    assert files, "Arquivo de log não foi criado"
    # Abre o arquivo de log e lê o conteúdo
    with open(files[0], "r") as f:
        content = f.read()
    # Verifica se a mensagem escrita está presente no conteúdo do log
    assert "Test log entry" in content
