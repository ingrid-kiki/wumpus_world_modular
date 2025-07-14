# ==============================
# benchmark/bm_fast_int.py (integrado com gráficos avançados)
# ==============================

import os
import time
import importlib.util
import numpy as np
from datetime import datetime
from utils.advance_graphs import gerar_graficos_avancados

def executar_benchmark(agentes, tamanhos, num_execucoes):
    resultados = {}

    if isinstance(tamanhos, int):
        tamanhos = [tamanhos]

    for nome in agentes:
        for tamanho in tamanhos:
            print(f"🏁 Executando agente '{nome}' em mundo {tamanho}x{tamanho}...")

            key = f"{nome}_{tamanho}x{tamanho}"
            resultados[key] = []

            for execucao in range(num_execucoes):
                print(f"  ➤ Execução {execucao+1}/{num_execucoes}")
                start_time = time.time()

                # Módulo do agente
                spec = importlib.util.spec_from_file_location("main", "main.py")
                main = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(main)

                resultado = main.executar_agente(nome, tamanho, execucao, benchmark=True)
                tempo_exec = time.time() - start_time
                resultado["tempo"] = tempo_exec

                resultados[key].append(resultado)

    # Coleta e salvamento dos gráficos
    now = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    output_dir = os.path.join("logs", now)
    os.makedirs(output_dir, exist_ok=True)

    for key, res_list in resultados.items():
        dados_extra = {
            "fitness": [],
            "fitness_pop": [],
            "fitness_final": [],
            "memoria": [],
            "cpu": [],
            "diversidade_vars": [],
            "pop_final": []
        }

        for resultado in res_list:
            if "dados_extra" in resultado:
                for k in dados_extra:
                    if k in resultado["dados_extra"]:
                        dados_extra[k].append(resultado["dados_extra"][k])

        # Empilha os dados corretamente (listas de execuções -> np.array ou 2D list)
        for k in dados_extra:
            if isinstance(dados_extra[k], list) and len(dados_extra[k]) > 0:
                try:
                    dados_extra[k] = np.array(dados_extra[k])
                except:
                    pass  # fallback para listas irregulares

        # Chama função de gráficos avançados
        gerar_graficos_avancados(dados_extra, output_dir)
