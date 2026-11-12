# Testes do projeto

Lista dos testes automáticos, com o que cada um garante. Situação em 11/11/2026: **175 casos de teste**, vindos de
**130 funções** em **24 arquivos** da pasta `tests/`.

Um teste parametrizado roda a mesma função com entradas diferentes. Cada entrada conta como um caso, e a coluna "Casos" mostra
quantos são.

## Como rodar

```bash
python -m pytest
```

```bash
python -m pytest tests/test_referencia.py
```

```bash
python -m pytest -k logico_seguro
```

O CI roda todos os testes a cada PR, no Ubuntu e no Windows, com Python 3.12 e 3.13, e exige pelo menos 78% de cobertura.

## Resumo por arquivo

| Arquivo | Casos | Foco |
|---|---|---|
| `test_referencia.py` | 9 | Resultados não mudam sem decisão explícita |
| `test_reprodutibilidade.py` | 13 | Metadados, reprodução de um run e otimizações do AG |
| `test_bugs_conhecidos.py` | 37 | Bugs corrigidos que não podem voltar |
| `test_entradas.py` | 24 | Entradas inválidas com mensagem clara |
| `test_constantes.py` | 3 | Ações, percepções e status num lugar só |
| `test_agente_base.py` | 13 | Classe base e lista única de agentes |
| `test_world.py` | 1 | Criação do mundo |
| `test_logic_agent.py` | 1 | Criação do agente lógico |
| `test_logico_seguro.py` | 16 | Agente lógico que evita poços |
| `test_manual_agent.py` | 1 | Criação do agente manual |
| `test_genetic_agent.py` | 1 | Criação e retorno do agente genético |
| `test_action_distribution.py` | 1 | O agente genético executa ações |
| `test_execution_time.py` | 1 | O agente genético termina em tempo razoável |
| `test_final_status.py` | 1 | O agente genético termina num estado válido |
| `test_fitness_history.py` | 1 | O agente genético registra o fitness |
| `test_trajectory_length.py` | 1 | O agente genético gera uma trajetória |
| `test_busca_aleatoria.py` | 6 | Busca aleatória, a referência do genético |
| `test_proximidade.py` | 9 | Bônus de proximidade ao ouro no fitness |
| `test_benchmark.py` | 4 | Benchmark único: modos sequencial e paralelo, silencioso e tempos |
| `test_main_etapas.py` | 7 | Arquivos de cada run e resistência a quedas |
| `test_graficos.py` | 9 | Gráficos nunca interrompem o benchmark |
| `test_experimento_31.py` | 7 | Script de comparação de métodos da #31 |
| `test_diagramas.py` | 7 | Diagrama de classes alinhado com o código |
| `test_lista_de_testes.py` | 2 | Esta lista alinhada com os testes |

## Resultados não mudam sem decisão

### `test_referencia.py`

Compara os resultados atuais com `tests/referencia.json`: mundos de tamanho 4, 6 e 8 com sementes 0 a 4. Para atualizar a
referência numa mudança intencional, veja o CONTRIBUTING.

| Teste | Casos | O que garante |
|---|---|---|
| `test_mundos_gerados_nao_mudam` | 1 | As posições do ouro, do Wumpus e dos poços de cada mundo continuam as mesmas |
| `test_resultados_do_agente_nao_mudam` | 4 | Vitórias, mortes e ações de `logico`, `genetico`, genético com proximidade e `aleatorio` continuam iguais |
| `test_regras_do_fitness_nao_mudam` | 1 | Sequências escritas à mão continuam com a mesma pontuação, inclusive matar o Wumpus |
| `test_decisoes_do_agente_logico_nao_mudam` | 1 | O agente lógico continua decidindo as mesmas ações nas situações de referência |
| `test_referencia_cobre_o_que_promete` | 1 | O cenário de referência tem todos os mundos e agentes declarados, com resultados variados |
| `test_referencia_detecta_mudanca` | 1 | Uma diferença em qualquer ação é detectada pelo resumo do histórico |

### `test_reprodutibilidade.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_parametros_do_ag_vem_da_linha_de_comando` | 1 | Opções como `--populacao` e `--cruzamento` viram os parâmetros do agente genético |
| `test_sem_opcoes_do_ag_valem_os_padroes` | 1 | Sem essas opções, o agente genético usa os próprios padrões |
| `test_benchmark_repassa_os_parametros_so_para_o_agente_certo` | 1 | Os parâmetros de um agente não chegam aos outros |
| `test_run_grava_metadata_completo` | 1 | O `metadata.json` traz versão, estado do git, argumentos, parâmetros do AG, sementes e bibliotecas |
| `test_sem_agente_genetico_nao_ha_parametros_do_ag` | 1 | Sem o agente genético no run, o `metadata.json` não inventa parâmetros do AG |
| `test_reproduzir_da_o_mesmo_resultado` | 1 | `reproduzir.py` refaz um run e encontra os mesmos resultados |
| `test_reproduzir_detecta_resultado_diferente` | 1 | `reproduzir.py` acusa um CSV adulterado |
| `test_reproduzir_sem_metadata` | 1 | `reproduzir.py` avisa quando a pasta não tem `metadata.json` |
| `test_sem_opcao_remove_opcao_e_valor` | 1 | Ao reproduzir, a opção `--saida` original é trocada pela nova pasta |
| `test_clone_do_mundo_e_independente` | 1 | Mexer na cópia do mundo não altera o original |
| `test_copia_do_individuo_e_independente` | 1 | Mexer na cópia de um indivíduo não altera o original |
| `test_cache_nao_muda_o_resultado_do_ag` | 1 | O cache de fitness não muda o resultado do AG, só evita simulações repetidas |
| `test_agente_genetico_com_parametros_da_cli_e_reprodutivel` | 1 | Duas execuções com os mesmos parâmetros dão as mesmas ações |

## Mundo, entradas e bugs corrigidos

### `test_bugs_conhecidos.py`

Cada teste descreve o comportamento correto de um bug já corrigido. Se algum falhar, o bug voltou.

| Teste | Casos | O que garante |
|---|---|---|
| `test_logico_mantem_posicao_sincronizada_com_o_mundo` | 1 | A base do agente lógico acompanha a posição real do agente no mundo (#18) |
| `test_kb_nao_sai_do_grid_mesmo_sem_a_posicao_do_mundo` | 1 | A base não "anda" para fora do mapa (#18) |
| `test_logico_sempre_termina` | 3 | Nos tamanhos 4, 6 e 8, o agente lógico vence, morre ou para no limite de passos (#18) |
| `test_mutacao_invalida_o_fitness` | 1 | Um indivíduo que sofreu mutação perde o fitness antigo (#19) |
| `test_fitness_do_melhor_individuo_corresponde_ao_cromossomo` | 5 | Em 5 sementes, o fitness do melhor indivíduo é o da sua própria sequência (#19) |
| `test_ouro_pontua_uma_vez_so` | 1 | Pegar o ouro conta pontos uma vez só (#20) |
| `test_mundo_nao_muda_depois_da_vitoria` | 1 | Depois de vencer, nenhuma ação muda o mundo (#20) |
| `test_mundo_nao_muda_depois_da_morte` | 1 | Depois de morrer, o agente continua morto e parado (#20) |
| `test_matar_o_wumpus_recebe_bonus` | 1 | Matar o Wumpus vale +25 no fitness (#21) |
| `test_tiro_sem_acertar_nao_recebe_bonus` | 1 | Errar o tiro só custa a ação (#21) |
| `test_pocos_nao_se_sobrepoem` | 1 | Em 900 mundos, há metade do tamanho em poços, sem repetir casa nem cair sobre o agente, o ouro ou o Wumpus (#22) |
| `test_world_nao_altera_o_random_global` | 1 | Criar um mundo não mexe no gerador aleatório global do Python (#23) |
| `test_mesma_semente_gera_o_mesmo_mundo` | 1 | A mesma semente sempre gera o mesmo mundo (#23) |
| `test_ag_reprodutivel_com_a_semente_do_mundo` | 1 | O AG dá o mesmo resultado qualquer que seja o estado do gerador global (#23) |
| `test_benchmarks_cumprem_o_contrato_do_main` | 2 | Nos modos sequencial e paralelo, o benchmark recebe e devolve os dados no formato que o `main.py` espera (#24) |
| `test_erro_nao_vira_resultado_nem_derruba_o_benchmark` | 2 | Nos dois modos, uma execução com erro entra em `erros` e as outras continuam (#30) |
| `test_dados_extra_vem_da_primeira_execucao_sem_erro` | 2 | Nos dois modos, se a primeira execução falha, os dados dos gráficos vêm da seguinte (#30) |
| `test_terminal_output_inclui_o_stderr` | 1 | Erros e avisos também vão para o `terminal_output.txt` (#30) |
| `test_benchmark_py_sozinho_nao_roda_o_agente_manual` | 1 | `python benchmark.py` não tenta rodar o agente manual, que precisa de teclado (#30) |
| `test_simular_execucao_preserva_dados_extra` | 1 | Uma execução isolada, como as do modo paralelo, não perde os dados dos gráficos (#24) |
| `test_csv_do_main_so_tem_colunas_escalares` | 1 | O CSV só tem números e nomes; os dados dos gráficos vão para o `.npz` (#24) |
| `test_traceback_do_modo_paralelo_chega_ao_terminal_output` | 1 | Com processos paralelos, o erro aparece uma vez no `terminal_output.txt` (#40) |
| `test_opcao_5_preserva_caminhos` | 6 | A opção 5 do menu mantém caminhos do Windows e do Linux, com e sem espaços e aspas (#39) |

### `test_entradas.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_mundo_rejeita_tamanho_invalido` | 3 | Tamanhos 1, 0 e −3 são recusados com mensagem, em vez de travar |
| `test_menor_mundo_valido_funciona` | 1 | O mundo 2x2 funciona e usa as quatro casas |
| `test_opcao_invalida_tem_mensagem_clara` | 13 | Valores errados de execuções, tamanhos, população, gerações, cromossomo, mutação, cruzamento, agente e arquivo de benchmark são recusados com mensagem clara |
| `test_opcoes_validas_nos_limites` | 1 | Valores nos limites são aceitos: 1 execução, mundo 2x2, população 1, 0 gerações, cromossomo 1, mutação 0 e cruzamento 1 |
| `test_opcoes_padrao_continuam_validas` | 1 | Sem opções, valem 32 execuções, tamanhos 4, 6 e 8 e os agentes `logico` e `genetico` |
| `test_menu_repete_ate_receber_tamanho_valido` | 1 | O menu pergunta de novo até receber um tamanho válido |
| `test_semente_em_branco_e_opcional` | 1 | Deixar a semente em branco é aceito |
| `test_semente_invalida_pergunta_de_novo` | 1 | Uma semente inválida faz o menu perguntar de novo |
| `test_execucao_unica_termina_com_entradas_corrigidas` | 1 | A execução única termina depois de respostas erradas seguidas de certas |
| `test_cromossomo_de_um_gene_nao_gera_erro` | 1 | Um cromossomo com um gene só não quebra o benchmark |

### `test_constantes.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_ordem_das_acoes_nao_muda` | 1 | A ordem das ações continua a mesma, porque os sorteios dos experimentos dependem dela |
| `test_deslocamentos_cobrem_os_movimentos_na_mesma_ordem` | 1 | Cada movimento tem um deslocamento, na mesma ordem da lista de movimentos |
| `test_nenhum_arquivo_escreve_acoes_percepcoes_ou_status_a_mao` | 1 | Fora de `world/constantes.py`, ações, percepções e status só aparecem pelas constantes |

### `test_world.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_world_initialization` | 1 | O mundo tem o tamanho pedido e as posições do agente, do ouro, do Wumpus e dos poços |

## Agentes

Os arquivos `test_world.py`, `test_logic_agent.py`, `test_manual_agent.py`, `test_genetic_agent.py`, `test_action_distribution.py`,
`test_execution_time.py`, `test_final_status.py`, `test_fitness_history.py` e `test_trajectory_length.py` são os testes mais antigos
do projeto. Eles verificam o mínimo, como a existência de atributos, e o comportamento fica coberto pelos testes acima e abaixo.

### `test_agente_base.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_agente_e_abstrato` | 1 | A classe base `Agente` não pode ser usada sozinha |
| `test_todos_os_agentes_herdam_de_agente` | 5 | Os cinco agentes da lista única herdam de `Agente` |
| `test_resultado_tem_o_formato_unico` | 4 | Os quatro agentes automáticos devolvem `historico`, `passos` e `dados_extra`, com passos numerados e a posição final certa |
| `test_agente_manual_devolve_o_formato_unico` | 1 | O agente manual também devolve o formato único |
| `test_executar_sequencia_para_no_fim_do_jogo` | 1 | Uma sequência de ações para quando o jogo termina, e cada passo guarda a posição |
| `test_main_e_benchmarks_usam_a_mesma_lista` | 1 | O `main.py` e o benchmark usam o mesmo dicionário de agentes |

### `test_logic_agent.py` e `test_manual_agent.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_logic_agent_initialization` | 1 | O agente lógico guarda o mundo, cria a base de conhecimento e tem o método `decide` |
| `test_manual_agent_receives_world` | 1 | O agente manual guarda o mundo recebido |

### `test_logico_seguro.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_vizinhas_de_casa_sem_brisa_sao_seguras` | 1 | Sem brisa numa casa, as vizinhas dela são seguras |
| `test_brisa_nao_torna_as_vizinhas_seguras` | 1 | Com brisa, as vizinhas não são consideradas seguras |
| `test_poco_certo_quando_so_uma_casa_explica_a_brisa` | 1 | O agente deduz o poço quando só uma casa pode explicar a brisa |
| `test_poco_nao_e_certo_com_duas_explicacoes` | 1 | Com duas explicações possíveis, nenhuma casa é dada como poço certo |
| `test_brilho_e_fedor_vem_antes_de_andar` | 1 | Pegar o ouro e atirar no Wumpus vêm antes de qualquer movimento |
| `test_prefere_casa_segura_a_casa_suspeita` | 1 | Entre uma casa segura e uma suspeita, o agente vai à segura |
| `test_anda_ate_casa_segura_distante_por_casas_visitadas` | 1 | O agente volta por casas já visitadas para alcançar uma casa segura distante |
| `test_sem_casa_segura_arrisca_e_nunca_escolhe_poco_certo` | 1 | Sem casa segura, o agente arrisca, mas nunca numa casa com poço certo |
| `test_sem_nada_a_fazer_fica_em_casas_conhecidas` | 1 | Sem nada a explorar nem a arriscar, o agente fica em casas conhecidas |
| `test_reproduz_os_numeros_registrados` | 3 | Em 1000 mundos de cada tamanho (4, 6 e 8), vitórias e mortes são exatamente as registradas na investigação |
| `test_nunca_morre_pelo_wumpus` | 1 | Em 300 mundos 6x6, o agente nunca morre pelo Wumpus |
| `test_registrado_no_programa_e_nos_benchmarks` | 2 | O agente está disponível no `main.py` e no benchmark |
| `test_roda_num_benchmark_pela_linha_de_comando` | 1 | `--agentes logico_seguro` roda um benchmark completo |

### `test_genetic_agent.py` e testes simples do agente genético

| Teste | Casos | O que garante |
|---|---|---|
| `test_genetic_agent_initialization` | 1 | O agente genético guarda os parâmetros e devolve histórico e dados para os gráficos |
| `test_action_distribution` | 1 | O agente genético executa pelo menos uma ação |
| `test_execution_time` | 1 | Com parâmetros pequenos, o agente genético termina em menos de 10 segundos |
| `test_final_agent_status` | 1 | O último status é `MORTO`, `GANHOU` ou `OK` |
| `test_fitness_history_tracking` | 1 | O agente genético devolve o histórico de fitness |
| `test_action_sequence_length` | 1 | O histórico de ações não é vazio |

### `test_busca_aleatoria.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_mesma_semente_mesmo_resultado_sem_depender_do_random_global` | 1 | A busca aleatória é reproduzível e não depende do gerador global |
| `test_executa_a_melhor_sequencia_e_respeita_o_orcamento` | 1 | Ela avalia exatamente o orçamento pedido e executa a melhor sequência |
| `test_fitness_informado_corresponde_a_sequencia_executada` | 1 | O fitness informado é o da sequência executada |
| `test_orcamento_zero_ainda_avalia_uma_sequencia` | 1 | Com orçamento zero, ainda avalia uma sequência, para ter o que executar |
| `test_benchmark_usa_o_mesmo_orcamento_do_ag` | 1 | No benchmark, o orçamento padrão é população × gerações do AG |
| `test_orcamento_explicito_tem_prioridade` | 1 | A opção `--avaliacoes` substitui o orçamento padrão |

### `test_proximidade.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_peso_zero_mantem_o_fitness_original` | 1 | Com peso 0, o fitness é exatamente o original |
| `test_bonus_cresce_com_a_proximidade` | 1 | Quanto mais perto do ouro, maior o bônus |
| `test_bonus_usa_a_menor_distancia_alcancada` | 1 | Afastar-se depois não tira o bônus de ter chegado perto |
| `test_bonus_conta_ate_a_morte` | 1 | O bônus considera o caminho feito até a morte |
| `test_ag_sem_proximidade_nao_muda` | 1 | Sem a opção, o AG dá o mesmo resultado de antes |
| `test_agente_com_proximidade_e_reprodutivel` | 1 | Com a opção, o agente genético é reproduzível |
| `test_opcao_chega_ao_agente_e_ao_metadata` | 1 | `--proximidade 20` aparece nos parâmetros efetivos do AG gravados no `metadata.json` |
| `test_sem_a_opcao_o_padrao_e_o_fitness_original` | 1 | Sem `--proximidade`, o `metadata.json` registra peso 0, isto é, o fitness original |
| `test_peso_negativo_e_recusado` | 1 | Peso negativo é recusado com mensagem clara |

## Programa principal, saídas e gráficos

### `test_benchmark.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_modos_sequencial_e_paralelo_dao_os_mesmos_resultados` | 1 | Com `logico_seguro` e `genetico`, os modos sequencial e paralelo dão as mesmas contagens |
| `test_silencioso_esconde_as_mensagens` | 1 | O modo silencioso não mostra as mensagens de cada execução nem de cada passo |
| `test_tempo_total_e_de_relogio_e_tempo_medio_e_a_media_das_execucoes` | 1 | `tempo_total` é o tempo de relógio e `tempo_médio`, a média das execuções |
| `test_opcoes_do_main_chegam_ao_benchmark` | 1 | `--paralelo` e `--silencioso` chegam ao benchmark, e sem elas nada é repassado |

### `test_main_etapas.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_layout_completo_de_um_run` | 1 | Um run grava todos os arquivos e pastas esperados, e nenhum arquivo `.log` |
| `test_queda_na_segunda_etapa_preserva_a_primeira` | 1 | Se uma combinação falha, os resultados das anteriores ficam gravados |
| `test_ctrl_c_tambem_preserva_resultados_e_log` | 1 | Interromper com Ctrl+C preserva os resultados e o registro no `terminal_output.txt` |
| `test_log_e_gravado_durante_a_execucao` | 1 | O `terminal_output.txt` é gravado durante a execução, e não só no fim |
| `test_graficos_avancados_valem_para_qualquer_agente_com_dados_extras` | 1 | Os gráficos avançados saem para qualquer agente que devolva dados para eles |
| `test_mensagem_conta_os_graficos_realmente_gerados` | 1 | A mensagem final informa quantos gráficos foram realmente gerados |
| `test_benchmark_externo_que_devolve_none_nao_derruba` | 1 | Um benchmark de terceiros que não devolve resultado não derruba o programa |

### `test_graficos.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_caso_normal_gera_os_nove_graficos` | 1 | Com dados completos, os 9 gráficos avançados são gerados |
| `test_dados_insuficientes_pulam_o_grafico` | 3 | Com um indivíduo, um gene ou zero gerações, os gráficos impossíveis são pulados sem erro |
| `test_falha_de_um_grafico_nao_impede_os_outros` | 1 | Se um gráfico falha, os demais são gerados |
| `test_falha_nos_graficos_basicos_nao_interrompe` | 1 | Uma falha nos gráficos básicos não interrompe o programa |
| `test_benchmark_termina_e_grava_os_resultados` | 3 | Nesses mesmos três casos, o benchmark termina e grava o CSV (#37) |

## Experimentos e documentação

### `test_experimento_31.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_resolvivel_reconhece_caminho_e_bloqueio` | 1 | Reconhece se há caminho até o ouro sem pisar em poço |
| `test_venceu_e_fitness_real_usam_o_mundo_sem_altera_lo` | 1 | Avaliar uma sequência não altera o mundo usado na comparação |
| `test_holm_ajusta_na_ordem_original` | 1 | A correção de Holm dá os valores esperados, na ordem original |
| `test_comparar_conta_mundos_discordantes` | 1 | A comparação pareada conta corretamente os mundos em que só um método venceu |
| `test_variante_truncamento_e_o_ag_do_projeto` | 1 | Sem variações, `AGVariante` dá o mesmo resultado do AG do projeto |
| `test_orcamento_do_ag_nao_e_ultrapassado` | 1 | O AG dos experimentos não passa do orçamento de avaliações |
| `test_tentar_devolve_uma_linha_completa` | 1 | Cada tentativa devolve todas as colunas da tabela de resultados |

### `test_diagramas.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_le_classes_declaradas_e_relacoes` | 1 | A leitura do diagrama encontra classes declaradas e citadas em relações |
| `test_membros_e_comentarios_nao_contam_como_classes` | 1 | Atributos, métodos e comentários não são confundidos com classes |
| `test_ignora_outros_tipos_de_diagrama` | 1 | Fluxogramas e outros diagramas são ignorados |
| `test_le_arquivo_com_quebra_de_linha_do_windows` | 1 | Arquivos salvos no Windows são lidos corretamente |
| `test_encontra_classes_do_programa_e_ignora_pastas_de_fora` | 1 | A leitura do código encontra as classes do programa e ignora `pygad/` e `tests/` |
| `test_nao_conta_classe_aninhada` | 1 | Classes dentro de funções ou de outras classes não contam |
| `test_diagrama_de_classes_bate_com_o_codigo` | 1 | Toda classe do diagrama existe no código, e toda classe do código está no diagrama |

### `test_lista_de_testes.py`

| Teste | Casos | O que garante |
|---|---|---|
| `test_lista_tem_todos_os_testes_com_os_casos_certos` | 1 | Todo teste existente está nesta lista, nenhum teste removido continua nela, e o número de casos de cada um está certo |
| `test_totais_da_lista_batem` | 1 | O resumo por arquivo e os totais do início desta página batem com os testes reais |

## Como manter esta lista

Ao criar, renomear ou remover um teste, atualize esta página na mesma PR. O teste `tests/test_lista_de_testes.py` falha
enquanto a lista estiver desatualizada e mostra o que mudou. Para ver os testes que o pytest encontra:

```bash
python -m pytest --collect-only -q
```
