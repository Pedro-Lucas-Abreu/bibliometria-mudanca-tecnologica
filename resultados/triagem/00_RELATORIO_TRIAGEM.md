# Triagem do corpus OpenAlex — polarizacao ocupacional (2000–2025)

## O que foi realizado

- Fonte: seis consultas OpenAlex `title_abstract_keywords`, selecionando `type:article` e 2000–2025; base congelada enviada pelo usuário.
- Populacao inicial: **3,468 registros unicos OpenAlex** (4.975 aparições nas seis buscas).
- Triagem de **todos os registros** por regras explícitas em título, resumo, campo e tipo de fonte.
- **120 registros amostrados foram examinados pelo título e trecho de resumo disponível**; não lemos o texto integral.
- Três saídas separadas: núcleo conservador **208**, revisão pendente **845**, não selecionados automaticamente **2,415**.

**O núcleo é PROVISÓRIO, não uma revisão sistemática definitiva:** a triagem automática não foi confirmada manualmente linha por linha, e existem documentos sem resumo, em outras línguas e erros de indexação.

## Regra econômica de inclusão

Incluem-se pesquisas sobre: mudanças relativas na participação de ocupações/empregos de baixa, média e alta remuneração ou qualificação (polarização, upgrading, hollowing out); mudança tecnológica baseada em tarefas/rotinização como explicação desses padrões; e evidência ocupacional relacionada a salários e desigualdade. A simples menção incidental a empregos, desigualdade ou IA não basta.

A classe **núcleo provisório** privilegia artigos de periódicos cujos títulos contêm o fenômeno estudado ou os mecanismos diretamente associados; alguns registros da amostra estratificada foram corrigidos qualitativamente.

**Revisar** significa que um documento potencialmente pertinente exige leitura mais atenta, ou sua fonte não confirma publicação em periódico. **Não selecionado** significa que as informações de busca e metadados não demonstram pertinência suficiente para o núcleo; não é uma sentença de irrelevância teórica.

## Auditoria do corpus

| Grupo | N | Artigos em periódicos | Sem referências indexadas | Sem país afiliado | Sem resumo | Títulos possivelmente duplicados |
|---|---:|---:|---:|---:|---:|---:|
| universo | 3,468 | 2,974 | 1,373 | 1,184 | 431 | 86 |
| nucleo_provisorio | 208 | 208 | 46 | 43 | 51 | 12 |
| revisar | 845 | 633 | 424 | 419 | 119 | 36 |
| nao_selecionado | 2,415 | 2,133 | 903 | 722 | 261 | 38 |


### Validação amostral estratificada

| Regra original | Incluir | Dúvida | Excluir | Total |
|---|---:|---:|---:|---:|
| A_titulo | 22 | 3 | 5 | 30 |
| B_resumo | 12 | 8 | 10 | 30 |
| C_topico_keyword | 13 | 9 | 8 | 30 |
| D_topico_resumo | 1 | 2 | 12 | 15 |
| E_nao_ancorado | 0 | 0 | 15 | 15 |


As proporções dessa amostra **não são taxa de precisão representativa dos 3.468**: há seleção estratificada em proporções diferentes das classes e reavaliação com metadados limitados. Necessária amostra de auditoria independente do núcleo final.

## Lacuna de cobertura que precisa constar no artigo

A busca não encontrou, entre os registros retornados, o clássico de Autor, Levy e Murnane (2003), *The Skill Content of Recent Technological Change: An Empirical Exploration*. Esse estudo pode entrar como **referência citada** na rede de acoplamento/cocitação sem estar no conjunto de artigos-fonte. Não afirmar que a base cobre toda a literatura de mudança tecnológica. Se ampliarmos a definição temática para incluir IA de modo geral, será necessária uma nova busca registrada e nova triagem.

## Como usar agora

1. Antes do VOSviewer: examinar `04_amostra_120_avaliada.csv`, especialmente os casos `duvida`, e `08_mais_citados_para_conferencia.csv`.
2. Abrir `02_nucleo_provisorio.csv` e inspecionar títulos de maior citação para confirmar a pertinência e possíveis duplicações por título e ano.
3. `05_nucleo_provisorio_openalex.json` mantém as entradas OpenAlex originais para teste de importação do VOSviewer; **compatibilidade efetiva do JSON com o assistente do VOSviewer não foi testada**.
4. Só depois de validar títulos/amostras e limpar sinônimos das palavras-chave consolidar mapas, comunidades e séries temporais.

### Limitações

- `type:article` da API não assegura artigo de periódico; a triagem privilegia `primary_location.source.type = journal`.
- Nomes e palavras-chave OpenAlex podem ser atribuídos por algoritmos. Não fundir títulos semelhantes sem checar DOI e versões.
- `referenced_works` ausente não significa que o artigo não cite obras; pode ser ausência de cobertura da base.
- Resultados são condicionais à consulta, não amostra aleatória da produção científica global.
- A classificação automática usa títulos/resumos/metadados; não se examinou texto integral, e trabalhos críticos com terminologia diferente podem estar de fora.
