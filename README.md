# Mudança tecnológica, polarização ocupacional e desigualdade salarial (2000–2025)

Repositório de dados, código, critérios documentais e resultados de uma **análise bibliométrica exploratória** da literatura sobre mudança tecnológica e polarização ocupacional (doutorado em Economia, UFSC).

## Situação atual — 18/11/2026

O **corpus documental harmonizado contém 326 obras únicas** (artigos/revisões de periódicos, publicações editoriais de 2000–2025). A base inicial tinha 3.468 registros únicos do OpenAlex, coletados por seis consultas. A seleção passou por triagem assistida, reconciliação de versões e harmonização documental; **não é uma revisão sistemática exaustiva nem uma leitura integral de 326 artigos**.

Resultados do cenário harmonizado (limiar de cinco artigos por palavra-chave): **91 termos**, **1.269 ligações**, **cinco comunidades Louvain** (semente 42), modularidade ponderada **Q = 0,11415**; **269 obras com referências indexadas**. Acoplamento dentro versus entre comunidades não apresentou diferença convincente (permutação bicaudal p ≈ 0,275). A interpretação depende das buscas e do corpus.

### Como reproduzir a versão atual

```powershell
python -m pip install -r requirements.txt
python scripts/10_reproduzir_corpus_326.py
```

O script usa apenas [a exportação original congelada do OpenAlex](dados/originais_openalex/07_openalex_uniao_vosviewer.json), [os 326 IDs selecionados](dados/harmonizado_326/ids_selecionados.txt) e as correções editoriais explicitadas no próprio código; **não precisa consultar a API**.

Os resultados atualizados são escritos em [resultados/harmonizado_326/](resultados/harmonizado_326/) (JSON do corpus, indicadores, tabelas e quatro figuras). O [workflow do GitHub Actions](.github/workflows/reproduzir_326.yml) executa a mesma rotina e publica as saídas quando tem permissão de escrita. Se a pasta ainda não estiver disponível, execute o comando localmente ou rode o workflow.

### Resultados e documentação

- [Relatório do corpus harmonizado de 326 obras](documentacao/13_HARMONIZACAO_METODOLOGICA_CORPUS_326_18NOV2026.md).
- [Fechamento dos 106 registros e base intermediária de 362 obras](documentacao/12_FECHAMENTO_106_CORPUS_362_17NOV2026.md).
- [Política de exclusões e versões duplicadas](documentacao/11_POLITICA_EXCLUSOES_243_17NOV2026.md).
- [Roteiro de revisão dos 845 pendentes](documentacao/08_REVISAO_DOCUMENTAL_ASSISTIDA_845_17NOV2026.md).
- [Critérios e pendências históricas](documentacao/02_METODOLOGIA.md).

### Versão histórica de 208 artigos

Os scripts `01`–`09`, o `executar_tudo.py` e o conteúdo das pastas `resultados/triagem/`, `resultados/analises/` e `resultados/rastreabilidade/` **permanecem preservados como cenário exploratório original de 208 artigos**, para transparência e comparação. Executar `python executar_tudo.py` **reproduz apenas a versão histórica**, não a versão vigente de 326 obras.

### Manuscrito

O manuscrito atualizado em LaTeX/PDF foi preparado separadamente; não faz parte deste repositório por opção de organização da pesquisa. Os resultados e a metodologia atualizada estão documentados aqui. O manuscrito anterior e a apresentação original utilizavam a base histórica de 208 e não devem ser confundidos com a análise harmonizada.

### Limitações

Faltam resumos indexados para 68 das 326 obras, DOI para 30 e referências indexadas para 57. Os 2.415 registros inicialmente não selecionados não foram auditados exaustivamente; uma amostra apontou possíveis falsos negativos. A rede depende dos termos indexados pelo OpenAlex, dos parâmetros do Louvain e da definição do corpus. A análise **não** estima efeitos causais da tecnologia sobre emprego ou salários.

URL pública: https://github.com/Pedro-Lucas-Abreu/bibliometria-mudanca-tecnologica
