# Métodos, parâmetros, fórmulas e limitações

## Pergunta de pesquisa provisória

Como se estrutura e evolui a literatura científica sobre mudança tecnológica e polarização ocupacional, e que conexões existem entre os núcleos de rotinização, automação e desigualdade salarial? IA e transição verde/digital são **linhas de expansão propostas**, ainda não cobertas satisfatoriamente pela coleta atual.

## Universo bibliográfico

Base secundária: OpenAlex, exportação congelada obtida por seis consultas independentes em título, resumo e keywords, `type:article`, anos 2000–2025. A API pode atualizar o índice, então a reprodução local usa o arquivo congelado recebido, não uma nova consulta. A classificação `type:article` **pode conter teses ou documentos incorretamente tipificados**; a triagem consulta também tipo de fonte e tipo documental original.

## Triagem documental

Regra implementada em `scripts/02_triagem.py`:

- Detecção de expressões específicas da polarização de empregos/ocupações ou mudança tecnológica orientada a tarefas no título, inclusive grafias de outros idiomas.
- Cruzamento com informação de tópico/área e fonte do periódico.
- Separação de homônimos como polarização política, física e títulos sem relação com polarização ocupacional.
- Aplicação de **rótulos históricos**, provenientes de uma amostra de 120 títulos/resumos, como ajustes pontuais explicitados no próprio código.
- Suspeitas de títulos duplicados **são sinalizadas**, não apagadas arbitrariamente.

A seleção de 208 é conservadora; trabalhos importantes podem ter ficado em `revisar` (845) ou mesmo em `nao_selecionado`, dependendo do padrão de indexação. A amostra é **provisória** e depende de validação científica adicional.

## Rede 1 — coocorrência de palavras-chave

- Nó: termo atribuído pelo OpenAlex e harmonizado por **seis aliases explícitos** no código.
- Filtro principal: palavra-chave presente em pelo menos **5 documentos** diferentes do núcleo provisório.
- Aresta não direcionada `(i,j)`: os dois termos são atribuídos ao **mesmo artigo**.
- Peso da aresta: número de documentos com ambos os termos.

Em notação simples, para os documentos `d` do conjunto `D`, `w(i,j) = soma_d 1[i em keywords(d)] × 1[j em keywords(d)]`.

As comunidades são detectadas pela rotina `networkx.community.louvain_communities` com peso `weight`, resolução 1 e semente 42. A modularidade é `networkx.community.modularity`, calculada sobre a mesma rede ponderada. O VOSviewer **não** é usado nesse passo, e não há equivalência automática dos clusters dos dois métodos.

Sensibilidade: repetição com limiares 3, 5 e 8 e com retirada da palavra de busca dominante `job polarization`. São testes de sensibilidade do algoritmo de visualização/análise, **não** estimativas de efeito econômico.

## Rede 2 — acoplamento bibliográfico

- Nós: artigos do corpus; sem referências OpenAlex, o artigo não consegue gerar ligações, embora ainda possa constar no total de publicações.
- Duas publicações são conectadas se compartilham referências bibliográficas identificadas pelo mesmo OpenAlex ID.
- Peso absoluto: quantidade de referências em comum, com corte de **pelo menos 2**.
- Similaridade normalizada de Salton: `S(i,j) = |refs_i ∩ refs_j| / sqrt(|refs_i| × |refs_j|)`.
- Para a visualização normalizada, selecionam-se **até 5 vizinhos mais similares por artigo**. É uma simplificação para legibilidade; a tabela integral com todas as arestas de peso 2+ é preservada.

Um artigo muito citado no corpus não é necessariamente a referência mais compartilhada; essas são medidas diferentes.

## Rede 3 — colaboração internacional

Países são obtidos de `authorships[].countries` e representam **afiliações institucionais**. Há ligação entre dois países quando aparecem juntos nas afiliações de ao menos um artigo. O peso é o número de documentos em que essa coafiliação ocorreu. Não representa a nacionalidade dos autores.

## Evolução temporal

Anos de publicação do OpenAlex; três intervalos descritivos 2000–2012, 2013–2018 e 2019–2025. Participação do tema é a razão entre número de documentos do **núcleo provisório** contendo pelo menos uma keyword do grupo e total de documentos desse núcleo no período.

As keywords são classificações do OpenAlex; não medem diretamente o conteúdo integral do estudo. Ainda não há evidência de que a distribuição de keywords na amostra conservadora represente todos os trabalhos de IA e transição verde/digital.

## O que precisa de revisão humana

1. Precisão e cobertura da triagem, especialmente 845 artigos em revisão e ausências de clássicos.
2. Possíveis títulos repetidos com IDs diferentes, DOI e versões.
3. Critérios de inclusão transparentes, idealmente com dupla codificação e amostra de auditoria independente.
4. Critérios adicionais de coleta para IA e transição verde/digital, se efetivamente incorporados à pergunta.
5. Estabilidade de temas/partições, incluindo índice de concordância de comunidades em especificações alternativas.

Nenhum desses itens pode ser omitido no artigo como se tivesse sido concluído.
