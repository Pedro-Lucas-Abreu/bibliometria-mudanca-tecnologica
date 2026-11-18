# Harmonização metodológica do corpus de 326 obras (18/11/2026)

**Status:** cenário bibliométrico harmonizado e reexecutado sobre metadados congelados. **Não constitui revisão sistemática com leitura integral ou dupla avaliação independente.** O corpus anterior de 362 obras permanece preservado.

## Critérios aplicados uniformemente
- Unidade: uma obra por publicação; traduções e versões duplicadas são reconciliadas, preferindo a publicação científica definitiva e a entrada bibliograficamente mais completa.
- Tipo documental: artigos/revisões em periódicos acadêmicos; working papers isolados, atas, teses, relatórios e divulgação não contam como artigos.
- Objeto: polarização ocupacional, composição ocupacional e mudança tecnológica relacionada a tarefas/qualificação/salários; não basta uma palavra-chave incidental.
- Ano: período editorial de 2000–2025; depósito em repositório não altera o ano efetivo de publicação.
- Histórico: cada exclusão e correção editorial permanece rastreável pelo ID OpenAlex.

## Resultados da auditoria dos 362

| Situação | Registros |
|---|---:|
| Retidos | **326** |
| Excluídos por tipo documental | 25 |
| Excluídos por tema fora do recorte | 3 |
| Versões duplicadas ou traduções da mesma obra | 6 |
| Edição definitiva em 2026, fora do período | 2 |
| **Total** | **362** |

**15 registros** tiveram veículo, ano ou DOI corrigidos sem inclusão automática. Houve correções de entradas OpenAlex rotuladas incorretamente como revista de entomologia, reconciliação de traduções da mesma obra de Valeria Cirillo e de um artigo colombiano, além de duas versões cuja publicação científica final é de 2026.

### Indicadores recalculados

| Indicador | 362 obras | 326 harmonizadas |
|---|---:|---:|
| Palavras-chave com frequência mínima 5 | 106 | **91** |
| Arestas de coocorrência | 1.618 | **1.269** |
| Comunidades (Louvain, semente 42) | 5 | **5** |
| Modularidade ponderada | 0,12128 | **0,11415** |
| Obras com referências indexadas | 279 | **269** |
| Pares com ≥2 referências compartilhadas | 23.668 | **22.418** |
| ARI médio entre 100 partições | 0,3612 | **0,4413** |

Nas 100 sementes, surgiram 5 comunidades em 61 execuções, 6 em 29, 4 em 8 e 7 em 2. Na comparação de acoplamento bibliográfico: **60,24% dos pares dentro dos grupos** versus **63,49% entre grupos**, diferença de −3,26 pontos percentuais; permutação bicaudal (999): **p≈0,275**. O estudo não detectou maior compartilhamento bibliográfico interno convincente nessa especificação; não prova equivalência ou consenso.

Em 2019–2025: automação 39/187 (20,9%); IA/aprendizado de máquina 9/187 (4,8%). Medem palavras-chave indexadas, não a evolução total da literatura mundial.

### Evidências editoriais ilustrativas
- *Polarization of the Nordic Labour Markets*: periódico *Finnish Economic Papers* (2011): https://ideas.repec.org/a/fep/journl/v24y2011i2p87-110.html
- *The Dynamics of Task-Biased Technological Change*: *Brussels Economic Review* (2013): https://ideas.repec.org/a/bxr/bxrceb/2013-186516.html
- *Technological intensity patterns and job polarization in Brazil's manufacturing industry*: *Revista Brasileira de Inovação* (2024): https://www.scielo.br/j/rbi/a/CmC8cRx4Gbhgj9B5v3bGDfJ/
- Traduções de artigo de Cirillo: registro ILO identifica versões linguísticas: https://researchrepository.ilo.org/esploro/outputs/journalArticle/La-polarisation-des-emplois-en-Europe/995219375102676
- Publicação editorial em 2026 de *Job polarisation with advent of technology*: https://www.inderscience.com/info/e_inarticletoc.php?issue=1&jcode=ijdipe&vol=12&year=2026

## Rastreabilidade e pendências

O pacote de análise entregue separadamente ao pesquisador contém **362 decisões**, corpus OpenAlex JSON de **326 obras**, histórico dos **3.468 registros originais**, auditoria de amostra **180 excluídos**, métricas, código Python reproduzível, figuras e Excel. **Esses arquivos não estão integralmente publicados neste repositório**; este Markdown é somente o registro da versão.

A amostra dos **2.415 registros anteriormente excluídos** apontou dois casos prioritários para reavaliação: David Autor (2019), *Work of the Past, Work of the Future*, e *The Skill Complementarity of Broadband Internet* (2015), além de sete casos secundários. **Eles não foram incluídos no corpus harmonizado**; a amostra não permite declarar cobertura exaustiva.

Limites atuais: **68/326** sem resumo indexado, **30/326** sem DOI, **57/326** sem referências indexadas. Não se conferiu manualmente o veículo editorial de todos os 326, nem se resolveu a cobertura das seis buscas originais. A análise de comunidades ainda depende da escolha das palavras-chave, do limiar e de empates na atribuição de artigos.

**Nome recomendado:** *corpus documental harmonizado de 326 obras — cenário conservador (2000–2025)*.

**Importante:** o artigo e o PPTX anteriores usam números do corpus de 208; é necessário atualizá-los antes de apresentar a nova versão como resultados finais.
