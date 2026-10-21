# Bibliometria da mudança tecnológica, polarização ocupacional e desigualdade salarial (2000–2025)

Projeto de pesquisa da disciplina de doutorado em Economia (UFSC), baseado em metadados do OpenAlex e análise de redes científicas.

**Estado: exploratório.** Foram recuperados 3.468 registros únicos. O núcleo de 208 trabalhos é **provisório** e 845 registros ainda requerem avaliação. As redes e seus agrupamentos não devem ser interpretados como resultados definitivos.

## Objetivo

Caracterizar a estrutura temática e intelectual da literatura sobre mudança tecnológica, tarefas, polarização ocupacional e desigualdade salarial, com revisão contextual de inteligência artificial e transição verde/digital.

## Dados e métodos

- Fonte: OpenAlex; período bibliométrico 2000–2025.
- Deduplicação e triagem documentada por registro.
- Coocorrência de palavras-chave, comunidades Louvain e sensibilidade a limiares.
- Acoplamento bibliográfico normalizado e colaboração entre países.
- Interpretação descritiva, sem pretensão de identificação causal.

## Indicadores exploratórios

| Indicador | Valor |
| --- | ---: |
| Registros únicos | 3.468 |
| Núcleo provisório | 208 |
| Revisão pendente | 845 |
| Rede de palavras-chave (limiar 5) | 56 nós, 545 arestas |
| Comunidades de palavras-chave | 5 |
| Modularidade | 0,1371 |
| Artigos com referências indexadas | 162 |
| Artigos com país identificado | 165 |

## Reprodutibilidade

O projeto completo utiliza Python 3.11+, pandas, NetworkX e matplotlib. A sequência dos oito scripts é administrada por `executar_tudo.py`.

## Observações metodológicas

A seleção de artigos e a interpretação das redes dependem de validação manual. Há artigos sem resumo, referências bibliográficas incompletas e casos de títulos duplicados. O núcleo provisório de 208 documentos não representa automaticamente toda a produção relevante.

## Fonte

OpenAlex (metadados bibliográficos). Referências individuais e direitos associados aos textos originais permanecem com seus titulares.
