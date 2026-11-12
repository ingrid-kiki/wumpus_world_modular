# Análise dos cinco arquivos de benchmark (novembro de 2026)

Relato de 11/11/2026. Ele apoia a decisão da tarefa 3.4 da Etapa 3 do [plano de boas práticas](plano-boas-praticas.md): trocar
os cinco arquivos de benchmark por um só. Nenhum código foi alterado por esta análise, e a decisão ainda é das autoras.

## 1. A pergunta

O projeto tem cinco arquivos que rodam benchmarks: `benchmark.py`, `benchmark_custom.py`, `benchmark_fast.py`,
`benchmark_graficos.py` e `benchmark_sideB.py`. Vale manter os cinco, ou trocar por um só?

## 2. O que cada arquivo faz

O núcleo dos cinco é o mesmo laço: criar o mundo com a semente da execução, rodar o agente com `executar_uma` e contar vitórias,
mortes, sobrevivências e erros. O que muda entre eles:

| Arquivo | Linhas | O que tem de próprio |
|---|---|---|
| `benchmark.py` | 77 | Nada: é o padrão do `main.py` |
| `benchmark_custom.py` | 112 | A opção `--silent`, que mostra menos mensagens |
| `benchmark_sideB.py` | 97 | Valores fixos no código: 10 execuções em 4x4, 6x6 e 8x8 |
| `benchmark_graficos.py` | 173 | Grava CSV e gráficos quando roda sozinho, o que o `main.py` já faz, junto com o `metadata.json` |
| `benchmark_fast.py` | 168 | Roda as execuções em processos paralelos, com `joblib`: a única diferença real de funcionamento |

Os quatro arquivos alternativos foram criados em julho de 2025 e alterados em 15 commits desde então.

## 3. Os resultados são os mesmos

Os cinco foram rodados nos mesmos mundos, com sementes 0 a N−1:

| Agente | Mundos | Vitórias, mortes, sobrevivências e erros |
|---|---|---|
| `logico` | 30 mundos 6x6 | 10, 20, 0 e 0 nos cinco arquivos |
| `logico_seguro` | 30 mundos 6x6 | 28, 2, 0 e 0 nos cinco arquivos |
| `genetico` (população 20, 15 gerações, cromossomo 20) | 10 mundos 4x4 | 6, 1, 3 e 0 nos cinco arquivos |
| `aleatorio` (300 avaliações, cromossomo 20) | 10 mundos 4x4 | 8, 1, 1 e 0 nos cinco arquivos |

O benchmark padrão completo também foi rodado com `benchmark.py` e com `benchmark_fast.py` (seção 4), e os resultados foram
idênticos: vitórias, mortes, sobrevivências e erros iguais nas seis combinações de agente e tamanho.

## 4. Tempo de execução

Trocar os cinco arquivos por um só **não deixa o modo normal mais rápido**: é o mesmo laço. O único ganho de velocidade vem do
modo paralelo, que hoje só existe no `benchmark_fast.py`.

Benchmark padrão completo, pelo `main.py`: agentes `logico` e `genetico`, tamanhos 4, 6 e 8, 32 execuções e os parâmetros padrão do
agente genético (população 100, 500 gerações, cromossomo 100). Computador com 12 núcleos lógicos, Windows 11 e Python 3.13.2:

| Modo | Arquivo | Tempo |
|---|---|---|
| Sequencial | `benchmark.py` | 258 s (4 min 18 s) |
| Paralelo | `benchmark_fast.py` | 102 s (1 min 42 s) |

O modo paralelo foi 2,5 vezes mais rápido. O ganho fica abaixo do número de núcleos porque o tempo do run inclui etapas que
rodam em sequência nos dois modos, como a gravação dos gráficos. Esse ganho não depende de trocar os cinco arquivos por um: ele já
existe com `--benchmark benchmark_fast.py`. Com um arquivo só, ele passa a ser uma opção de qualquer run.

Duas observações da medição:

- O plano registrava até 12 minutos para o benchmark padrão; nesta medição ele levou 4 min 18 s. A diferença não foi investigada.
- No modo paralelo, a coluna `tempo_total` do CSV soma o tempo de cada execução, e não o tempo de relógio: deu 324 s para o agente
  genético nos três tamanhos, num run que levou 102 s.

Em execuções curtas o paralelo piora: nos testes da seção 3, ele gastou cerca de 6 segundos a mais só para iniciar os processos.
Por isso ele deve ser uma opção, e não o padrão.

## 5. O custo de manter os cinco

- **São 627 linhas para um único comportamento.** A função `executar_benchmark` aparece cinco vezes, e a geração de gráficos de
  `benchmark_fast.py` e `benchmark_graficos.py` repete o que `utils/graficos.py` já faz.
- **Cada correção vale em cinco lugares.** Os bugs [#24](https://github.com/ingrid-kiki/wumpus_world_modular/issues/24) e
  [#30](https://github.com/ingrid-kiki/wumpus_world_modular/issues/30) foram corrigidos nos cinco arquivos.
- **Cada agente novo exige seis alterações.** A lista de agentes existe no `main.py` e nos cinco arquivos. Para o `logico_seguro`
  entrar, foi preciso alterar os seis.
- **Os testes repetem a mesma verificação.** 20 casos de teste existem só porque há cinco arquivos: três testes de
  `test_bugs_conhecidos.py` rodam cinco vezes cada, e o registro do `logico_seguro` é conferido em cinco benchmarks.
- **Há risco de divergência.** Se um arquivo for corrigido e outro não, os resultados da tese passam a depender de qual arquivo foi
  usado.

## 6. Opções

| Opção | O que acontece | Preserva | Perde |
|---|---|---|---|
| 1. Um só, com `--paralelo` | Um benchmark com as opções `--paralelo` e de menos mensagens; os outros quatro arquivos saem | Os números, o paralelismo, o modo silencioso, CSV e gráficos pelo `main.py`, e a opção `--benchmark` para arquivos externos | Os comandos diretos, como `python benchmark_graficos.py`; README e tutorial precisam mudar |
| 2. Um só, com atalhos finos | Como a opção 1, mas os quatro arquivos ficam com poucas linhas cada, chamando o benchmark único | Tudo da opção 1 e os comandos antigos | Quatro arquivos a mais na raiz do projeto |
| 3. Manter os cinco | Nada muda | Tudo | Os custos da seção 5 continuam |

Nas opções 1 e 2, o teste de referência garante que os números não mudam. A estimativa é que o código de benchmark caia de 627
para cerca de 150 linhas; esse valor só será conhecido depois da mudança.

## 7. Decisão

**Decidido em 11/11/2026:** opção 1. Implementada na PR D da Etapa 3
([#76](https://github.com/ingrid-kiki/wumpus_world_modular/pull/76)): o `benchmark.py` ganhou os modos `paralelo` e
`silencioso`, o `main.py` ganhou as opções `--paralelo` e `--silencioso`, e os outros quatro arquivos saíram. O código de
benchmark passou de 627 para 100 linhas. `tempo_total` passou a ser o tempo de relógio nos dois modos.

## 8. Como repetir as medições

As duas medições usaram os scripts abaixo, salvos fora do projeto e executados a partir da raiz do repositório, no commit `d76b95e`.
Eles importam os quatro arquivos que saíram na #76, então só rodam a partir desse commit ou da tag `v1.8.0`.

<details>
<summary>Comparação dos resultados nos cinco arquivos (seção 3)</summary>

```python
"""Roda executar_benchmark dos 5 arquivos nos mesmos mundos e compara contagens e tempo."""

import contextlib
import io
import os
import sys
import time
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import benchmark  # noqa: E402
import benchmark_custom  # noqa: E402
import benchmark_fast  # noqa: E402
import benchmark_graficos  # noqa: E402
import benchmark_sideB  # noqa: E402

AG = {"genetico": {"population_size": 20, "gens": 15, "chrom_length": 20}}
for agente, tam, n in (("logico", 6, 30), ("logico_seguro", 6, 30), ("genetico", 4, 10), ("aleatorio", 4, 10)):
    print(f"\n{agente} {tam}x{tam}, {n} execuções")
    for modulo in (benchmark, benchmark_custom, benchmark_fast, benchmark_graficos, benchmark_sideB):
        inicio = time.perf_counter()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            r = modulo.executar_benchmark(
                agente, tam, n, parametros_agentes={**AG, "aleatorio": {"avaliacoes": 300, "chrom_length": 20}}
            )
        contagem = (r["vitórias"], r["mortes"], r["sobreviveu"], r["erros"])
        print(
            f"  {modulo.__name__:20s} vitórias/mortes/sobreviveu/erros = {contagem} | {time.perf_counter() - inicio:5.1f}s"
        )
```

</details>

<details>
<summary>Tempo do benchmark padrão em sequência e em paralelo (seção 4)</summary>

```python
"""Roda o benchmark padrão completo em sequência (benchmark.py) e em paralelo (benchmark_fast.py) e mede o tempo."""

import json
import os
import platform
import sys
import time
from pathlib import Path

raiz, saida = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
os.environ["MPLBACKEND"] = "Agg"
os.chdir(raiz)
sys.path.insert(0, str(raiz))
import main  # noqa: E402
import reproduzir  # noqa: E402

medidas = {"cpus": os.cpu_count(), "plataforma": platform.platform(), "python": platform.python_version()}
for nome, arquivo in (("sequencial", "benchmark.py"), ("paralelo", "benchmark_fast.py")):
    inicio = time.perf_counter()
    main.rodar_benchmark(["--benchmark", arquivo, "--saida", str(saida / nome)])
    medidas[nome] = round(time.perf_counter() - inicio, 1)
    (saida / "medidas.json").write_text(json.dumps(medidas, indent=2), encoding="utf-8")

iguais, tabela = reproduzir.comparar(
    saida / "sequencial" / "resultados_benchmark.csv", saida / "paralelo" / "resultados_benchmark.csv"
)
medidas["resultados_iguais"] = bool(iguais)
medidas["tabela"] = tabela.to_string(index=False)
(saida / "medidas.json").write_text(json.dumps(medidas, indent=2, ensure_ascii=False), encoding="utf-8")
```

</details>
