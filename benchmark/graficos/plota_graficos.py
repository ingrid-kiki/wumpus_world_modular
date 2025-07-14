import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

def plot_fitness_history():
    path = os.path.join(RESULTS_DIR, "fitness_history.csv")
    if os.path.exists(path):
        print(f"Lendo {path}")
        data = pd.read_csv(path, header=None, names=["Fitness"])
        print(data.head())
        if not data.empty:
            plt.figure(figsize=(8, 4))
            sns.lineplot(data=data, x=data.index, y="Fitness")
            plt.title("Evolução do Fitness")
            plt.xlabel("Geração")
            plt.ylabel("Fitness")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(RESULTS_DIR, "grafico_fitness.png"))
            plt.close()
        else:
            print("Arquivo fitness_history.csv está vazio.")
    else:
        print(f"Arquivo {path} não encontrado.")

def plot_action_distribution():
    path = os.path.join(RESULTS_DIR, "action_distribution.log")
    if os.path.exists(path):
        print(f"Lendo {path}")
        with open(path, "r") as f:
            line = f.read()
            if "📊 Distribuição de ações: " in line:
                raw = eval(line.split("📊 Distribuição de ações: ")[-1].strip())
                data = pd.DataFrame(list(raw.items()), columns=["Ação", "Frequência"])
                print(data.head())
                if not data.empty:
                    plt.figure(figsize=(8, 4))
                    sns.barplot(data=data, x="Ação", y="Frequência")
                    plt.title("Distribuição de Ações Executadas")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.savefig(os.path.join(RESULTS_DIR, "grafico_acoes.png"))
                    plt.close()
                else:
                    print("Nenhuma ação encontrada no arquivo.")
            else:
                print("Formato inesperado em action_distribution.log.")
    else:
        print(f"Arquivo {path} não encontrado.")

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plot_fitness_history()
    plot_action_distribution()
    print("✅ Gráficos gerados em:", RESULTS_DIR)

if __name__ == "__main__":
    main()
