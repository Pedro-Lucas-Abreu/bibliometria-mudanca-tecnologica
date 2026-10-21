# Origem e auditoria das informações

## 1. O que recebemos do usuário

**OpenAlex, coleta já realizada pelo usuário** com `openalex_unificar_validar.py`. Os sete arquivos originais foram preservados sem alterações em `dados/originais_openalex/`. Seus hashes SHA-256 estão em `dados/manifest_sha256.json`.

| Arquivo | Significado | Uso no projeto |
|---|---|---|
| `01_base_unificada.csv` | Tabela resumida dos 3.468 OpenAlex IDs únicos | Reconciliação e triagem textual |
| `02_auditoria_buscas.csv` | 6 expressões e contagens do site e da API | Reconciliação das 4.975 aparições |
| `03_sobreposicao_buscas.csv` | Sobreposição entre pares de buscas | Inspeção de duplicatas entre consultas |
| `04_producao_anual.csv` | Produção no universo coletado | Diagnóstico da coleta, **não** da amostra filtrada |
| `05_frequencia_keywords.csv` | Frequência de keywords no universo amplo | Diagnóstico da coleta |
| `06_amostra_para_validar.csv` | Amostra criada na etapa original | Histórico da seleção |
| `07_openalex_uniao_vosviewer.json` | Registro completo da união de resultados e metadados OpenAlex | Principal origem das referências, autores, países e keywords |

As seis expressões, com filtro 2000–2025, tipo `article`, usando busca em título/resumo/keywords, são `job polarization`, `employment polarization`, `occupational polarization`, `labor market polarization`, `routine-biased technological change`, `routine-biased technical change`.

O número **4.975** soma os retornos das seis consultas, **não** registros únicos. A comparação e retirada de sobreposições por `OpenAlex ID` gera **3.468 IDs únicos** e **1.507 aparições excedentes**. Não equivale à remoção de publicações duplicadas por título/DOI.

## 2. A seleção não é um fato observável nem uma triagem humana definitiva

A triagem antiga foi refeita com regras de título, resumo, palavra-chave, tópico e tipo de fonte contidas em `scripts/02_triagem.py`. Um conjunto de **120 rótulos de julgamento anterior** é aplicado às mesmas linhas de uma amostra estratificada, guardada em `dados/insumos_triagem/amostra_120_estratificada.csv`.

**Importante para apresentação:** os 120 rótulos derivam de uma etapa anterior de revisão assistida, são históricos e não devem ser apresentados como revisão independente por múltiplos especialistas. É inadequado afirmar que todos os 3.468 títulos foram examinados manualmente ou que os 208 já são o corpus final validado.

A rotina classifica provisoriamente em 208 `nucleo_provisorio`, 845 `revisar`, 2.415 `nao_selecionado`. **Cada uma das 3.468 decisões** está em `resultados/triagem/01_decisoes_3468.csv`, ao lado da variável `justificativa_regra`. Uma revisão humana dos casos pendentes ainda pode alterar os totais.

## 3. Da amostra provisória às redes

| Resultado mostrado | Arquivos de origem | Procedimento reproduzível | Saída |
|---|---|---|---|
| 208 artigos e 845 pendentes | CSV/JSON OpenAlex + amostra histórica | `scripts/02_triagem.py` | `resultados/triagem/` |
| Keywords e sua frequência | campo `keywords` dos 208 documentos do JSON | `scripts/03_redes_e_figuras.py` | `resultados/analises/ranking_termos.csv` |
| Coocorrência 56 nós/545 ligações | palavras-chave atribuídas a cada artigo | `scripts/03_redes_e_figuras.py` | `fig2_rede_keywords.png` |
| Comunidades e modularidade Louvain | rede ponderada de coocorrência | `scripts/03_redes_e_figuras.py` | `indicadores.json` e `clusters_keyword.csv` |
| Automação por período | `publication_year` e keywords de cada artigo | `scripts/03_redes_e_figuras.py` | `temas_periodos.csv` e `fig3_temas_por_periodo.png` |
| Acoplamento bibliográfico | campo `referenced_works` de cada artigo | `scripts/03_redes_e_figuras.py`, `04_acoplamento_normalizado.py` | `fig4_rede_acoplamento.png`, `fig5_acoplamento_normalizado_k5.png` |
| Países/colaboração | `authorships[].countries` (afiliações) | `scripts/03_redes_e_figuras.py` | `indicadores.json` |
| Origem de cada aresta | IDs de artigos/referências nos JSON | `scripts/07_rastrear_resultados.py` | `resultados/rastreabilidade/` |
| Primeira rede exploratória VOSviewer | dois CSVs exportados pelo usuário | `scripts/05_rede_vosviewer_original.py` | `resultados/vosviewer_exploratorio/` |

## 4. Exemplo para demonstrar uma ligação ao professor

1. Abra `resultados/analises/fig2_rede_keywords.png` e escolha dois termos conectados.
2. No arquivo `resultados/rastreabilidade/03_arestas_keyword_com_documentos.csv`, procure a dupla de termos nas colunas `keyword_1` e `keyword_2`.
3. A coluna `peso_coocorrencia` informa em quantos artigos eles aparecem juntos.
4. A coluna `artigos_openalex_ids` exibe **os IDs exatos dos artigos** que dão origem à aresta.
5. No arquivo `resultados/rastreabilidade/06_artigos_nucleo_e_metadados.csv`, localize um desses IDs para mostrar título, ano, keywords e referências indexadas.

**Acoplamento**: abra `04_arestas_acoplamento_com_referencias.csv` e mostre as duas publicações e os `referencias_openalex_ids` compartilhados. Assim, cada peso da rede tem procedência auditável.

## 5. O que NÃO podemos inferir

- Mudança da frequência de keywords na amostra filtrada **não** prova um aumento da produção mundial sobre aquela tecnologia.
- País de afiliação não é nacionalidade do autor.
- Vínculo de duas palavras-chave não implica concordância teórica nem influência causal.
- Ausência de referências indexadas no OpenAlex não demonstra ausência de referências no artigo.
- A versão presente em `resultados/analises/` **não é** a rede original calculada no VOSviewer; o seu algoritmo de comunidades é distinto.
