# Reunião de quinta-feira — roteiro de demonstração pelo VS Code

## Objetivo

Mostrar uma **análise em execução e reproduzível**, com pergunta econômica, dados brutos, critérios e evidências da implementação. **Não** dizer que já existe um artigo final revisado.

## Uma apresentação de 5 a 8 minutos

**1. Problema econômico (60 s)** — “Quero mapear como a literatura econômica conectou polarização ocupacional, mudança tecnológica baseada em tarefas, desigualdade salarial e automação. Estou analisando a estrutura temática e intelectual dos artigos, não estimando efeitos causais da tecnologia sobre o emprego.”

**2. Coleta (60 s)** — Abrir `dados/originais_openalex/02_auditoria_buscas.csv` e apontar as seis expressões, 4.975 retornos somados e 3.468 trabalhos únicos no JSON. Abrir `scripts/01_validar_fontes.py` e `resultados/auditoria/conferencia_coleta.json`.

**3. Filtro crítico (60 s)** — Abrir `scripts/02_triagem.py` e `resultados/triagem/01_decisoes_3468.csv` para mostrar as regras por documento e o núcleo de 208. Dizer explicitamente que é **provisório** e que outros 845 precisam de revisão. Enfatizar que palavras-chave do OpenAlex trouxeram ruído de outras áreas.

**4. Resultados temáticos (90 s)** — Abrir `resultados/analises/fig2_rede_keywords.png` e `resultados/analises/fig3_temas_por_periodo.png`. Mostrar 56 keywords e 545 ligações (min 5); os percentuais são **dentro da amostra filtrada**. Abrir `scripts/03_redes_e_figuras.py` para mostrar o cálculo real. Não confundir Louvain com clusters do VOSviewer.

**5. Resultado adicional (60 s)** — Abrir `resultados/analises/fig5_acoplamento_normalizado_k5.png` e `resultados/rastreabilidade/04_arestas_acoplamento_com_referencias.csv`. Explicar “dois artigos se conectam por referências que compartilham”. Mostrar as referências exatas de uma linha.

**6. Resultado rastreável (60 s)** — Abrir `resultados/rastreabilidade/03_arestas_keyword_com_documentos.csv` e escolher um par de palavras. A coluna `artigos_openalex_ids` permite rastrear o peso da aresta aos documentos brutos.

**7. Encerramento (30 s)** — Apontar `resultados/resumo_reproducibilidade.json` e o relatório gerado automaticamente em Markdown. “O próximo passo é validar a população de artigos e aprofundar a extensão para IA/transição dupla, como sugerido.”

## Perguntas que podem aparecer

**Por que os 208?** São regras conservadoras transparentes, não um número escolhido pelo resultado. O universo bruto tem 3.468; 845 ainda exigem avaliação. O tamanho final da amostra **poderá mudar**.

**Por que bibliometria?** É uma pergunta de estrutura e evolução da produção científica e pode ser tratada com redes de keywords, referências e coautoria, sem prometer identificação causal que esses dados não fornecem.

**Quais são os pontos fracos?** Termos de busca, classificação automática, lacunas de cobertura de referências, ausência de alguns clássicos, eventual duplicação de títulos e baixa cobertura de IA/verde.

**As cinco comunidades são o resultado final?** Não. Cinco no VOSviewer da busca exploratória inicial e cinco no Louvain sobre a base de 208 são resultados distintos de corpora/algoritmos diferentes. Ambas ainda são exploratórias.

**Vai incluir transição verde?** É uma expansão relevante, mas ainda precisa de busca complementar registrada e definição de como se encaixa na pergunta econômica.

## Dica prática

Use **Ctrl+Shift+V** para visualizar o relatório Markdown, enquanto deixa aberta a aba do script correspondente. Isso deixa lado a lado uma figura e sua origem calculada.
