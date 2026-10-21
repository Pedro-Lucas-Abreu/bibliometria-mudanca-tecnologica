# ESQUELETO DE ARTIGO — bibliometria e revisão narrativa

> Versão de trabalho para discussão com Dominik em 22/10/2026. **Não é manuscrito final.** Os resultados quantitativos são provisórios e derivam do corpus de 208 documentos ainda não integralmente validado.

## Título provisório

**Mudança tecnológica, polarização ocupacional e desigualdade salarial: estrutura temática e intelectual da literatura, 2000–2025**

**Extensão proposta, ainda não mensurada na base principal:** impactos da inteligência artificial e da transição verde/digital sobre tarefas, ocupações e desigualdade.

## 0. Resumo — escrever por último

[Contexto e lacuna — 2 frases.]  
[Pergunta de pesquisa — 1 frase.]  
[OpenAlex, seis buscas, período e regras de triagem — 2 frases.]  
[Redes de palavras-chave, acoplamento bibliográfico, evolução temporal, colaboração por afiliação — 1–2 frases.]  
[Resultados revisados após validação — 2 frases.]  
[Contribuição, limitações e agenda IA/verde — 1–2 frases.]

**Palavras-chave:** polarização ocupacional; mudança tecnológica; tarefas rotineiras; bibliometria; desigualdade salarial; redes científicas.

## 1. Introdução

### 1.1 Motivação econômica

A literatura explica a reorganização do emprego a partir da mudança tecnológica enviesada por qualificação e por tarefas, automação e deslocamentos setoriais. Há interesse em saber como essas explicações passaram a dialogar com desigualdade salarial e novas tecnologias.

### 1.2 Pergunta principal

**Como se estruturam e evoluem os vínculos temáticos e intelectuais na literatura sobre mudança tecnológica e polarização ocupacional entre 2000 e 2025?**

Subperguntas:
- Quais termos e conjuntos de trabalhos aparecem conectados no corpus recuperado?
- Como a incidência de temas indexados muda entre períodos, com cautela sobre cobertura e seleção?
- Quais trabalhos compartilham bases bibliográficas e como os autores se conectam por afiliação institucional?
- Como uma revisão narrativa pode interpretar o debate atual sobre IA e a transição verde/digital sem extrapolar os resultados bibliométricos?

### 1.3 Contribuição pretendida

Caracterização **descritiva e rastreável** da produção científica recuperada; articulação entre evolução temática e literatura econômica selecionada. **Não** medir efeitos causais da tecnologia sobre emprego ou salários.

## 2. Revisão de literatura — desenvolver antes de concluir a interpretação das redes

### 2.1 Mudança tecnológica enviesada por qualificação e tarefas

Contrastar SBTC, RBTC e o enfoque baseado em tarefas. Incluir e ler **Autor, Levy e Murnane (2003)** como fundamento teórico, embora o clássico não esteja entre os 208 documentos-fonte: https://doi.org/10.1162/003355303322552801.

### 2.2 Polarização ocupacional, demanda por trabalho e desigualdade salarial

Distinguir polarização do **emprego** e desigualdade **salarial**; diferenciar variações nas participações relativas e variações absolutas. Situar Autor, Katz e Kearney (2006), Goos e Manning (2007), Autor e Dorn (2013), Goos, Manning e Salomons (2014). Confirmar referências antes da versão final.

### 2.3 Offshoring, automação, robótica e heterogeneidade das exposições

Sintetizar mecanismos complementares ou concorrentes; explicar por que uma proximidade temática não prova um mecanismo econômico.

### 2.4 Inteligência artificial — avanço recente, por enquanto revisão narrativa

Diferenciar tarefas potencialmente automatizadas, ocupações expostas, produtividade, complementaridade, substituição e distribuição salarial. Leitura inicial: Gmyrek, Berg e Bescond (OIT, 2023), *Generative AI and Jobs* — https://doi.org/10.54394/FHEM8239. **Não afirmar que a atual coleta de seis buscas mapeou toda a produção sobre IA.**

### 2.5 Transição dupla — verde e digital

Explicar o conceito e sua relação com emprego, demanda por competências, transição entre ocupações e desigualdades territoriais. Leitura inicial: JRC (2022), *Towards a Green & Digital Future* — https://publications.jrc.ec.europa.eu/repository/handle/JRC129319; OCDE (2024), *Employment Outlook: The Net-Zero Transition and the Labour Market* — https://doi.org/10.1787/ac8b3538-en. **No estágio atual, seção de contexto/agenda, não resultado de rede.**

### 2.6 Hipótese interpretativa, não resultado presumido

Examinar se o corpus recuperado documenta deslocamento de linguagem e perguntas de pesquisa, das qualificações e tarefas para automação e tecnologias recentes. A seleção e os metadados precisam ser auditados antes de qualquer afirmação sobre toda a literatura.

## 3. Dados e metodologia

### 3.1 Fonte, protocolo de busca e período

OpenAlex; seis consultas em título/resumo/keywords, 2000–2025; documentação completa das strings, filtros, datas e exportação congelada.

### 3.2 Deduplicação e triagem

4.975 ocorrências entre buscas -> 3.468 IDs únicos -> 208 no **núcleo provisório**, 845 pendentes e 2.415 não selecionados. Explicar regras, tratamentos de títulos repetidos e plano de auditoria humana. **Não nomear o estudo como revisão sistemática concluída.**

### 3.3 Rede de coocorrência de palavras-chave

Nó = keyword do OpenAlex; aresta = coocorrência no mesmo documento; peso = número de documentos. Mínimo de cinco documentos por keyword no mapa principal. Clusters por Louvain e modularidade ponderada; critérios de limpeza de sinônimos, análise com limiares 3/5/8 e sem termo âncora.

### 3.4 Acoplamento bibliográfico

Nó = artigo; conexão = referências compartilhadas. Salton = referências comuns / raiz(produto do total de referências de cada artigo). Filtro k=5 apenas para visualização. **Não confundir acoplamento bibliográfico com cocitação. Cocitação ainda não é uma análise final implementada neste pacote.**

### 3.5 Colaboração internacional

País corresponde à afiliação institucional recuperada, não à nacionalidade de cada pesquisador. Explicitar cobertura faltante.

### 3.6 Limitações de inferência

Redes são descritivas; resultados dependem de indexação, consulta, filtro e parâmetros. OpenAlex pode classificar keywords automaticamente. Ausência de referências indexadas não significa ausência de citações no documento.

## 4. Resultados exploratórios — conferir contra uma única versão reproduzível

### 4.1 Caracterização da amostra

Tabelar universo, núcleo e pendências. Inserir `fig1_producao_anual.png` e não generalizar contagens ao universo sem validar a triagem.

### 4.2 Rede temática e sensibilidade

56 termos (freq. >= 5), 545 arestas, cinco comunidades; modularidade **0,1371** conforme `resultados/RELATORIO_REPRODUZIVEL.md` do projeto. Interpretar como associação temática observada, sem declarar comunidades estáveis ou escolas de pensamento já validadas. Figura `fig2_rede_keywords.png`.

### 4.3 Evolução dos termos

No núcleo atual, a keyword `automation` aparece em 0/28 (2000–12), 6/71 (2013–18) e 14/109 (2019–25). Tratar como **indexação dentro do corpus**, não como crescimento populacional da literatura. Figura `fig3_temas_por_periodo.png`.

### 4.4 Acoplamento bibliográfico e colaboração

162/208 artigos com referências indexadas; 8.775 pares com duas ou mais referências comuns antes do filtro de visualização. Afiliação de país presente em 165/208; 50 com ao menos dois países. Inserir `fig5_acoplamento_normalizado_k5.png` e analisar documentos centrais com validação bibliográfica.

## 5. Discussão

O que o padrão de coocorrências acrescenta à leitura dos artigos clássicos? Como ligar tarefas, polarização, offshoring e salários sem transformar conexões em causalidade? Onde IA e transição verde/digital podem gerar **novas perguntas**? Que estudos importantes ficaram fora da coleta (ex.: Autor, Levy e Murnane, 2003)?

## 6. Limitações e agenda de extensão

- Auditoria ainda necessária nos 208 incluídos e 845 pendentes.
- Recuperação incompleta de clássicos e potencial perda de trabalhos por termos de busca.
- Cobertura parcial de referências, abstracts, afiliações e keywords.
- Resultado de modularidade depende do ambiente/versão; harmonizar números do PDF anterior com a última reprodução.
- Caso IA/verde passem a fazer parte das redes, definir **buscas adicionais pré-especificadas**, novo protocolo e triagem simétrica; não misturar os corpora silenciosamente.
- Revisão narrativa sobre IA/verde não deve ser confundida com comprovação bibliométrica do surgimento dessas áreas.

## 7. Conclusão — rascunhar somente após validação

Reafirmar pergunta, contribuição descritiva, padrões corroborados e limites; apresentar agenda de pesquisa sem alegar causalidade.

## Quatro decisões a negociar na reunião

1. O trabalho será bibliometria **com** uma seção narrativa de revisão, ou uma revisão de literatura com mapas como apoio?
2. IA/verde entram apenas como discussão recente nesta entrega ou justificam uma expansão formal da coleta?
3. Quanto de revisão humana é necessário para declarar um corpus final suficientemente confiável dentro do prazo?
4. Quais são os 2–3 gráficos/achados que devem estruturar a contribuição do artigo?
