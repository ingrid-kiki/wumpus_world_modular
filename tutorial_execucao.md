# 📘 Tutorial de Execução - Projeto Wumpus World com Agentes Inteligentes

Este guia mostra como executar o projeto **Wumpus World**, incluindo o uso dos diferentes agentes (manual, lógico, genético), visualização gráfica com Pygame e benchmarks automatizados.

---

## ✅ 1. Pré-requisitos

- Python 3.8 ou superior
- Pip instalado

---

## ✅ 2. Instalar dependências

Abra o terminal no diretório do projeto e execute:

```bash
pip install pygame
```

---

## ✅ 3. Executar o jogo com agentes

### 📌 Sintaxe básica

```bash
python main.py [AGENTE] [--size N] [--seed VALOR] [--vis]
```

### 🧠 Agentes disponíveis

| Nome       | Descrição                                      |
|------------|-----------------------------------------------|
| `manual`   | Controlado pelo usuário via terminal           |
| `logico`   | Regras simples com mapa interno                |
| `genetico` | IA baseada em algoritmo genético               |

---

### 🎮 Exemplos

```bash
python main.py manual
```

```bash
python main.py logico --size 4 --vis
```

```bash
python main.py genetico --size 6 --seed 42
```

---

## ✅ 4. Como controlar o agente manual

Digite as ações no terminal:

```text
Ação (CIMA, BAIXO, ESQUERDA, DIREITA, AGARRAR, TIRO): up
```

---

## ✅ 5. Visualização com Pygame

Use `--vis` para ativar a interface gráfica:

```bash
python main.py logico --vis
```

---

## ✅ 6. Executar o Benchmark

Roda 20 execuções automáticas dos agentes lógicos e genéticos:

```bash
python benchmark.py
```

Exemplo de saída:

```
📊 RESULTADOS - Agente: LOGICO
🏆 Vitórias: 11 (55.0%)
☠️ Mortes: 5 (25.0%)
⏱️ Tempo médio: 0.10 segundos
```

---

## ✅ 7. Onde ver os logs?

Os arquivos de log são salvos automaticamente na pasta:

```
/logs/
├── logico_YYYYMMDD_HHMMSS.log
├── genetico_YYYYMMDD_HHMMSS.log
```

---

## ✅ 8. Estrutura do Projeto

```
.
├── agents/           # Agentes manuais, lógicos e genéticos
├── ga/               # Algoritmo genético
├── world/            # Lógica do mundo do Wumpus
├── visual/           # Visualização com Pygame
├── utils/            # Logger
├── logs/             # Gerado automaticamente
├── main.py           # Executa o jogo
├── benchmark.py      # Executa testes comparativos
└── README.md
```

---

## 💡 Dica extra

Quer repetir o mesmo cenário para testes? Use:

```bash
python main.py logico --seed 123
```

---

## 👩‍💻 Autoria

Este projeto é mantido por **Alfa Marine** e **Ingrid Mendes**, com foco em IA, jogos e ensino computacional.