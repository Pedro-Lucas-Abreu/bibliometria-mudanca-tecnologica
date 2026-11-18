# Corpus ampliado de 324 obras — processamento de 17/11/2026

**Status:** cenário computacional reexecutado com as 121 decisões de inclusão aceitas, conforme instrução do pesquisador. **Não substitui silenciosamente os resultados dos 208 artigos publicados anteriormente.** Os 243 registros inconclusivos seguem separados.

## Seleção e duplicações
- Núcleo anterior: **208 IDs OpenAlex**.
- Candidatos aceitos da segunda triagem: **121 IDs**.
- Corpus antes de reconciliar versões: **329 IDs**.
- **Cinco pares de versões duplicadas** (já presentes nos 208 originais) foram conciliados por título, autores, DOI e tipo de publicação. Resultado: **324 obras únicas**.
- Das outras propostas, **481 exclusões foram aceitas**, mas **243 seguem inconclusivas**: 111 por pertinência, 49 sem resumo, 72 para confirmar a fonte e 11 por duplicidade.
- Os **2.415 inicialmente não selecionados** permanecem na classificação original.

## Comparação dos resultados

| Indicador | Núcleo anterior (208 IDs) | Corpus ampliado (324 obras) |
|---|---:|---:|
| Palavras-chave com frequência ≥5 | 56 | **96** |
| Arestas de coocorrência | 545 | **1.373** |
| Louvain (semente 42) | 5 comunidades | **5 comunidades** |
| Modularidade ponderada | 0,1371 | **0,1250** |
| Artigos com referências indexadas | 162 | **247** |
| Pares com ≥2 referências em comum | 8.775 | **18.921** |
| Fração desses pares | 67,3% | **62,3%** |
| Artigos com países de afiliação | 165 | **252** |

A nova rotina refez os cálculos sobre os **208 originais** antes de calcular o cenário ampliado e reproduziu exatamente os indicadores-chave publicados, o que permite atribuir as diferenças à seleção e às duplicações, não à mudança do algoritmo.

## Robustez da nova rede
- Louvain com **100 sementes**: cinco comunidades em **47** execuções e seis em **53**.
- ARI médio entre partições: **0,4523**; modularidade variou de **0,1147** a **0,1289**.
- Na atribuição de cada artigo à comunidade predominante das suas keywords, **66 dos 247** artigos com referências tiveram empate.
- Pares com ≥2 referências em comum: **64,1% dentro** das comunidades e **61,3% entre** elas; diferença **+2,8 pontos percentuais**; teste de permutação bicaudal com 999 permutações: **p≈0,358**. Não se encontrou diferenciação convincente.

## Mudanças temáticas
- Keyword de automação, 2013–2018: **8 de 102 (7,8%)**, comparados a 6/71 (8,5%) anteriormente.
- Keyword de automação, 2019–2025: **34 de 185 (18,4%)**, comparados a 14/109 (12,8%) anteriormente.
- Grupo de keywords de IA (inclui machine learning), 2019–2025: **12 de 185 (6,5%)**, comparados a 3/109 (2,8%) anteriormente.

Os indicadores se referem a palavras-chave atribuídas pelo OpenAlex, não a efeitos de tecnologia no mercado de trabalho. A seleção tem impacto material na distribuição dos temas e na comparação dentro/entre comunidades.

## Rastreabilidade e arquivos produzidos

O processamento local gerou:
- corpus CSV de **324 obras** e JSON OpenAlex correspondente;
- rastreio individual dos **3.468** registros;
- documentação dos cinco pares de versões reconciliados;
- tabela de comparação entre **208, 203 deduplicados, 329 brutos e 324 únicos**;
- 100 sementes Louvain, referências mais utilizadas, acoplamento e evolução temática;
- quatro figuras novas, um arquivo Excel e um script Python independente com verificações das métricas anteriores.

**Importante:** os arquivos completos do cenário e o novo script foram disponibilizados em um pacote para download ao pesquisador, separadamente. **Este registro Markdown não publica nem substitui os CSVs/JSONs e scripts no repositório GitHub.** Para reproduzir o cenário, incorporar ao projeto os arquivos do pacote e rodar `python scripts/10_cenario_expandido.py`.

## Limitações

As inclusões e exclusões foram **assumidas como corretas** para continuar a análise; não houve leitura integral nem dupla revisão independente de cada documento. Os 243 casos inconclusivos permanecem em aberto, e o corpus expandido não deve ser descrito como uma revisão sistemática exaustiva.

A normalização alternativa de coocorrência, um modelo nulo de rede com preservação de graus e revisão da atribuição dos artigos em caso de empate não foram realizados. Os resultados anteriores do manuscrito e dos slides continuam ligados ao corpus antigo e requerem atualização antes de serem apresentados como números do corpus ampliado.
