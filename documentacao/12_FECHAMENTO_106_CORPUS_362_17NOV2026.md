# Fechamento dos 106 registros e cenário de 362 obras

**Processamento iniciado em 17/11/2026.** Estado: **triagem documental conservadora concluída para a fila de 106**, mas não revisão sistemática baseada em leitura integral.

## Critério desta etapa
Incluir somente artigo ou revisão especializada em periódico de pesquisa com relação substantiva a polarização ocupacional, mudança tecnológica relacionada a tarefas/SBTC/RBTC, composição ocupacional e/ou desigualdade salarial ligada a esses mecanismos. Excluir versões duplicadas, registros sem evidência suficiente de pertinência ou que sejam relatórios, livros, teses, working papers e divulgação não publicada como artigo científico. Nos pares, preferir a edição editorial definitiva. O conteúdo das decisões é rastreado por ID OpenAlex.

## Decisões sobre os 106

| Decisão | Registros |
|---|---:|
| Inclusões aceitas | **38** |
| Exclusão por tipo documental | 48 |
| Exclusão por pertinência fora do recorte | 10 |
| Exclusão por versão duplicada | 10 |
| **Total** | **106** |

Alguns casos aceitos: *Polarization or upgrading? Evolution of employment in transitional Russia*; *The Vanishing Middle*; *Polarization of the Nordic Labour Markets*; *Technological intensity patterns and job polarization in Brazil's manufacturing industry*; *The “task approach” to labor markets: an overview*; *Digitalization, routineness and employment*; *The exposure to routinization* e estudos recentes sobre rotinização na Índia e China.

Duplicatas identificadas com versões já presentes nos 324: *The Trend is the Cycle: Job Polarization and Jobless Recoveries* (versão científica definitiva publicada na **Review of Economics and Statistics**), *Wage Shocks and Technological Substitution*, *Automation and Job Polarization: On the Decline of Middling Occupations in Europe*, e outras. Não foram somadas novamente.

**Correções documentais adicionais:** *Upskilling and polarisation in the Australian labour market* é artigo de 2011 apesar de depósito OpenAlex de 2024; *Explaining Women's Success* tem edição de periódico em 2010 em lugar da cópia de repositório de 2007; *The exposure to routinization* é artigo de periódico de 2022; *Employment Shares across Occupations in the Online Labour Market* tem edição de 2025. Uma correspondência sugerida anteriormente entre um artigo chinês de 2015 e o ID **W45024973** foi rejeitada: esse ID refere-se a artigo em japonês.

## Balanço dos 845 e universo original

- Entre os **845** inicialmente pendentes: **159 inclusões** (121 na rodada anterior + 38 agora) e **686 exclusões operacionais** (481 na rodada anterior + 137 da política conservadora + 68 agora). Não restam decisões pendentes nesta fila.
- Dos **208** IDs originais, cinco representavam segundas versões de trabalhos já selecionados, deixando **203 obras**.
- **203 obras originais + 159 inclusões = 362 obras únicas**.
- Reconciliação dos 3.468 registros únicos: **362 selecionados + 686 excluídos nos 845 + 2.415 anteriormente não selecionados + 5 versões retiradas do núcleo original = 3.468**.

## Indicadores do cenário de 362

| Indicador | 324 obras | **362 obras** |
|---|---:|---:|
| Palavras-chave com frequência ≥5 | 96 | **106** |
| Arestas de coocorrência | 1.373 | **1.618** |
| Comunidades na semente 42 | 5 | **5** |
| Modularidade ponderada | 0,1250 | **0,12128** |
| Obras com referências indexadas | 247 | **279** |
| Pares que compartilham ≥2 referências | 18.921 | **23.668** |

Em 100 sementes do Louvain, houve **5 comunidades em 44 execuções, 6 em 49, 4 em 2 e 7 em 5**, com ARI médio **0,3612**. Ao atribuir artigos à comunidade predominante de suas keywords, ocorreram **58 empates** entre as 279 obras com referências. A proporção de pares que compartilham ≥2 referências é **60,17% dentro** e **61,53% entre** grupos, diferença de **-1,36 p.p.**, com permutação bicaudal (999): **p=0,628**. A direção da diferença mudou novamente em relação aos 324; portanto, não há evidência convincente nesta especificação de separação bibliográfica forte.

Para a janela 2019–2025, keyword de automação: **42/206 (20,4%)**; IA/machine learning: **14/206 (6,8%)**. Os percentuais dependem da coleta, seleção e indexação OpenAlex.

## Arquivos reproduzíveis

Foram produzidos, **fora do GitHub e disponibilizados em pacote ZIP na conversa**:
- Planilha `FECHAMENTO_106_CORPUS_362.xlsx`: 106 decisões, justificativas, fontes, subconjuntos e cenário de 362;
- `01_decisoes_finais_106.csv`;
- `02_corpus_cenario_324_mais_106_resolvidos.csv`;
- `03_rastreabilidade_3468.csv`;
- `indicadores_362/corpus_362_openalex.json` e os demais resultados;
- script independente `REPRODUZIR_CORPUS_362.py` com 100 sementes Louvain, teste de permutação, gráficos e indicadores. Requer `networkx` e `matplotlib` e não precisa acessar API.

Este registro Markdown **não significa** que esses dados e scripts completos tenham sido adicionados ao GitHub.

## Limites ainda importantes

1. A classificação foi conduzida por título, resumos/sínteses, metadados e fontes documentais, **não** leitura integral ou dupla avaliação independente de 845 estudos.
2. O núcleo original de **324** foi preservado, mas pode conter relatórios/working papers sob a triagem original; falta **harmonizar o tipo documental** caso o objetivo seja um corpus estritamente de artigos de periódico.
3. Os **2.415** registros inicialmente não selecionados não foram auditados integralmente para falsos negativos.
4. Alguns anos editoriais do núcleo de 324 ainda divergem do ano OpenAlex; a evolução temporal é exploratória até reconciliação sistemática.
5. A rede e suas comunidades são sensíveis à inclusão de estudos, ao vocabulário e aos empates; p-valores de permutação não comprovam equivalência bibliográfica.

**Conclusão:** encerramos operacionalmente a fila dos 845, produzindo um cenário de **362 obras** e novas análises. Não chamar de revisão sistemática exaustiva nem substituir resultados anteriores sem atualizar artigo e slides.
