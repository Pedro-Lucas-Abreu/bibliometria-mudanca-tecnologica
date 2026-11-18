# Segunda triagem assistida — 17/11/2026

**Status: protocolo e listas de prioridade gerados; seleção final ainda NÃO validada.**

Esta auditoria reavaliou os metadados do arquivo congelado [01_decisoes_3468.csv](../resultados/triagem/01_decisoes_3468.csv), sem alterar o núcleo bibliométrico original nem as redes já publicadas. A unidade de análise permanece o OpenAlex ID.

## Resultado de priorização dos 845 registros pendentes

| Categoria de revisão | N |
|---|---:|
| Candidatos prioritários a conferir para eventual inclusão | 156 |
| Candidatos a leitura temática do resumo | 163 |
| Fonte/tipo de publicação a verificar | 91 |
| Sem resumo suficiente para decidir | 90 |
| Possível duplicidade ou problema documental | 51 |
| Pertinência ainda incerta e prioridade baixa | 293 |
| Exclusão preliminar por assunto aparentemente fora do recorte | 1 |
| **Total** | **845** |

Essas categorias são uma **ordem de trabalho**, não decisões finais. Não houve inclusão nem exclusão automática no corpus. Os registros sem resumo e possíveis duplicatas podem aparecer em outras categorias, como alertas independentes: 119 sem resumo, 48 com título potencialmente duplicado e 1 com DOI repetido no universo de 3.468.

## Núcleo de 208 e revisão dos excluídos

Dos 208 trabalhos anteriormente selecionados, 64 acionaram ao menos um alerta de qualidade ou pertinência (51 sem resumo, 12 títulos/DOIs potencialmente duplicados, 9 sem sinais suficientes nas novas regras; há sobreposições). **Isso não significa que 64 sejam inadequados**, nem que os demais já estejam validados.

Para investigar possíveis falsos negativos nos 2.415 originalmente não selecionados, foi preparada uma amostra de **120 registros aleatórios estratificados por regra original**, sem reutilizar os IDs dos 120 registros examinados na triagem histórica, e **60 casos adicionais direcionados** por indícios de pertinência. A amostra direcionada não deve ser tratada como probabilística.

## Critérios e próximos passos

1. Conferir título, resumo, DOI e natureza documental dos candidatos prioritários, registrando justificativa para incluir, excluir ou manter em dúvida.
2. Resolver suspeitas de duplicação confrontando DOI, versões e fontes.
3. Auditar os 208 atuais e as amostras dos excluídos para detectar possíveis erros de seleção.
4. Revisar os casos ambíguos e sem resumo diretamente na fonte, recorrendo ao texto integral apenas quando necessário.
5. Construir **novo corpus somente após confirmação das decisões humanas**, mantendo o original preservado; então reexecutar coocorrência, Louvain, acoplamento e análises temporais.

### Exemplos que merecem revisão temática

- *Why Are There Still So Many Jobs? The History and Future of Workplace Automation*
- *The “task approach” to labor markets: an overview*
- *Where Have the Middle-Wage Workers Gone? A Study of Polarization Using Panel Data*
- *The Polarization Myth: Occupational Upgrading in Germany, Spain, Sweden, and the UK, 1992–2015*

Esses exemplos aparecem entre os **845 pendentes** e não foram automaticamente incluídos.

## Ressalvas de validade

O procedimento utiliza apenas metadados textuais e regras explícitas de palavras-chave, título, resumo e fonte. Ele não é uma leitura integral ou revisão manual independente, nem estima a precisão da triagem. A amostra histórica de 120 registros usada para ajustar o protocolo inicial não pode servir como validação independente do mesmo protocolo.

A auditoria produziu uma planilha de trabalho com sugestões por registro, seus motivos e campos de decisão humana, além dos respectivos CSVs e um script reproduzível. **Esses novos arquivos de trabalho foram entregues separadamente ao pesquisador; não fazem parte do corpus ou dos resultados publicados nesta versão do repositório.** Os resultados originais de 208 artigos devem continuar identificados como exploratórios até a revisão documental.

Não utilizar esta auditoria para alegar revisão sistemática concluída nem para afirmar que todas as propostas foram conferidas manualmente.
