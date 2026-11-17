# ==============================
# ga/ga_core.py
# ==============================
# Este arquivo implementa o núcleo do algoritmo genético utilizado pelo AgenteGenetico
# no projeto Wumpus World. Define a classe AlgoritmoGenetico, responsável por criar,
# evoluir e selecionar populações de indivíduos (soluções), aplicando operadores de
# seleção, cruzamento e mutação para buscar sequências de ações que maximizem o desempenho
# do agente no ambiente. Serve como base para experimentos de IA evolutiva no projeto.

import os
import random
from typing import Any

import numpy as np
import psutil

# Importa a classe Individuo (representa um possível agente/solução)
from world.constantes import ACOES
from world.world import Mundo

from .individual import Individuo, fitness_de

ELITE = 2  # os melhores indivíduos passam intactos para a próxima geração
CANDIDATOS_A_PAI = 10  # a seleção sorteia os pais entre os melhores desta quantidade
BYTES_POR_MB = 1024 * 1024


class AlgoritmoGenetico:
    def __init__(
        self,
        tamanho_populacao: int,
        geracoes: int,
        tamanho_cromossomo: int,
        taxa_mutacao: float,
        taxa_cruzamento: float,
        semente: int | None = None,
        proximidade: float = 0.0,
    ) -> None:
        # Gerador próprio, para o AG ser reprodutível sem depender do random global (#23)
        self.gerador = random.Random(semente)
        # Peso do bônus de proximidade ao ouro no fitness; 0 mantém o fitness original (#31)
        self.proximidade = proximidade
        # Tamanho da população de indivíduos
        self.tamanho_populacao = tamanho_populacao
        # Número de gerações (iterações do algoritmo)
        self.geracoes = geracoes
        # Tamanho do cromossomo (quantidade de ações em cada indivíduo)
        self.tamanho_cromossomo = tamanho_cromossomo
        # Taxa de mutação padrão
        self.taxa_mutacao = taxa_mutacao
        # Taxa de cruzamento padrão
        self.taxa_cruzamento = taxa_cruzamento
        # Fitness mínimo, médio e máximo por geração: {'minimo': x, 'media': y, 'maximo': z}
        self.historico_fitness: list[dict[str, float]] = []
        # Histórico do fitness de toda a população por geração (para gráficos avançados)
        self.fitness_populacao: list[list[float]] = []
        # Histórico de uso de memória por geração
        self.historico_memoria: list[float] = []
        # Histórico de uso de CPU por geração
        self.historico_cpu: list[float] = []
        # Diversidade de genes por posição no cromossomo
        self.historico_diversidade: list[list[int]] = []
        # Cache de fitness por cromossomo: o mundo não muda durante a evolução, então o mesmo
        # cromossomo tem sempre a mesma nota. Não altera o resultado, só evita simular de novo.
        self._cache_fitness: dict[tuple[str, ...], float] = {}
        self.avaliacoes = 0  # simulações realmente executadas
        self.acertos_cache = 0  # avaliações respondidas pelo cache

    def avaliar(self, individuo: Individuo, mundo: Mundo) -> None:
        """Define individuo.fitness, simulando só cromossomos ainda não vistos."""
        chave = tuple(individuo.cromossomo)
        if chave in self._cache_fitness:
            individuo.fitness = self._cache_fitness[chave]
            self.acertos_cache += 1
        else:
            individuo.avaliar(mundo, self.proximidade)
            self._cache_fitness[chave] = fitness_de(individuo)
            self.avaliacoes += 1

    def executar(self, mundo: Mundo) -> dict[str, Any]:
        """Evolui a população por `geracoes` gerações no mundo dado e devolve o melhor indivíduo e os históricos."""
        # Cada execução começa com o cache vazio (o cache vale para um mundo só)
        self._cache_fitness = {}
        self.avaliacoes = 0
        self.acertos_cache = 0
        # Registra o uso de memória e CPU antes de iniciar as gerações
        processo = psutil.Process(os.getpid())
        processo.cpu_percent()

        # Cria a população inicial de indivíduos aleatórios
        populacao = [Individuo(self.tamanho_cromossomo, self.gerador) for _ in range(self.tamanho_populacao)]
        for _ in range(self.geracoes):
            self._registrar_recursos(processo)
            # Avalia o fitness de cada indivíduo e ordena do melhor para o pior
            for ind in populacao:
                self.avaliar(ind, mundo)
            populacao.sort(key=fitness_de, reverse=True)
            self._registrar_geracao(populacao)
            populacao = self._proxima_geracao(populacao)

        # Avalia todos da última geração (caso tenha novos filhos não avaliados)
        for ind in populacao:
            if ind.fitness is None:
                self.avaliar(ind, mundo)
        melhor_individuo = max(populacao, key=fitness_de)
        return self._resultado(melhor_individuo, populacao)

    def _registrar_recursos(self, processo):
        """Guarda o uso de memória (MB) e de CPU (%) no início de uma geração."""
        self.historico_memoria.append(processo.memory_info().rss / BYTES_POR_MB)
        self.historico_cpu.append(processo.cpu_percent())

    def _registrar_geracao(self, populacao):
        """Guarda a diversidade de genes por posição e o fitness da população já ordenada."""
        # Quantos genes diferentes há em cada posição do cromossomo, em toda a população
        diversidade_geracao = [len({ind.cromossomo[i] for ind in populacao}) for i in range(self.tamanho_cromossomo)]
        self.historico_diversidade.append(diversidade_geracao)

        valores_fitness = [ind.fitness for ind in populacao]
        self.historico_fitness.append(
            {
                "minimo": min(valores_fitness),
                "media": sum(valores_fitness) / len(valores_fitness),
                "maximo": max(valores_fitness),
            }
        )
        self.fitness_populacao.append(valores_fitness.copy())

    def _proxima_geracao(self, populacao):
        """Elitismo, seleção, cruzamento e mutação: monta a próxima geração a partir da atual, já ordenada."""
        proxima = populacao[:ELITE]  # os melhores passam intactos
        while len(proxima) < self.tamanho_populacao:
            p1, p2 = self.selecionar(populacao), self.selecionar(populacao)
            if self.gerador.random() < self.taxa_cruzamento:
                c1, c2 = self.cruzar(p1, p2)
            else:
                c1, c2 = p1.copia(), p2.copia()  # sem cruzamento, os filhos são cópias dos pais
            self.mutar(c1)
            self.mutar(c2)
            proxima.extend([c1, c2])
        return proxima[: self.tamanho_populacao]  # o último par pode passar do tamanho

    def _resultado(self, melhor_individuo, populacao):
        """Resultado de executar(): o melhor indivíduo, a população final e os históricos para os gráficos."""
        return {
            "melhor": melhor_individuo,
            "historico_fitness": self.historico_fitness,
            "fitness_pop": self.fitness_populacao,
            "populacao_final": [ind.cromossomo for ind in populacao],
            "memoria": self.historico_memoria,
            "cpu": self.historico_cpu,
            "diversidade_vars": np.array(self.historico_diversidade),
            "avaliacoes": self.avaliacoes,
            "acertos_cache": self.acertos_cache,
        }

    def selecionar(self, populacao: list[Individuo]) -> Individuo:
        # Seleciona aleatoriamente um indivíduo entre os 10 melhores (seleção por truncamento)
        return self.gerador.choice(populacao[:CANDIDATOS_A_PAI]).copia()

    def cruzar(self, p1: Individuo, p2: Individuo) -> tuple[Individuo, Individuo]:
        # Realiza o cruzamento de dois pais para gerar dois filhos
        if self.tamanho_cromossomo < 2:  # com um gene só não há ponto de corte possível (#38)
            return p1.copia(), p2.copia()
        ponto = self.gerador.randint(1, self.tamanho_cromossomo - 1)  # Ponto de corte aleatório
        c1 = Individuo(0)
        c2 = Individuo(0)
        # Combina partes dos cromossomos dos pais para formar os filhos
        c1.cromossomo = p1.cromossomo[:ponto] + p2.cromossomo[ponto:]
        c2.cromossomo = p2.cromossomo[:ponto] + p1.cromossomo[ponto:]
        return c1, c2

    def mutar(self, individuo: Individuo) -> None:
        mudou = False
        for i in range(self.tamanho_cromossomo):
            # Aplica mutação com base na taxa de mutação
            if self.gerador.random() < self.taxa_mutacao:
                individuo.cromossomo[i] = self.acao_aleatoria()
                mudou = True
        if mudou:
            # O cromossomo mudou: o fitness herdado do pai não vale mais (#19)
            individuo.fitness = None

    def acao_aleatoria(self) -> str:
        # Gera uma ação aleatória válida para o cromossomo
        return self.gerador.choice(ACOES)
