# Conferência dos 72 registros de fonte e 49 registros sem resumo (17/11/2026)

**Escopo:** a partir da segunda triagem de 845 registros OpenAlex, foram pesquisados externamente os 72 classificados como `VERIFICAR_FONTE` e os 49 classificados como `REVISAR_SEM_RESUMO`. Os 111 registros com pertinência temática duvidosa foram mantidos **fora do corpus principal, por decisão conservadora**, mas não tratados como irrelevantes.

## Resultado
- **61/72** fontes editoriais ou institucionais relacionadas identificadas em pesquisa externa; **11** sem confirmação suficientemente confiável.
- **18** dos 72 registros vinculados a periódicos (isso **não significa** 18 obras adicionais elegíveis, devido a versões repetidas e ao critério temático).
- **40/49** registros antes sem abstract receberam **sínteses curtas em português fundamentadas em fonte externa**, **não transcrições** dos resumos originais; **9** não tiveram evidência textual suficiente.
- **324 obras** do cenário ampliado permanecem **inalteradas**, assim como suas redes.

## Achados e riscos
- *Upskilling and Polarisation in the Australian Labour Market* tem publicação editorial **2011**, embora sua cópia institucional apareça como **2024** no OpenAlex ([RePEc](https://ideas.repec.org/a/fli/journl/26014.html)).
- *Automation and Job Polarization: On the Decline of Middling Occupations in Europe* aparece em duas versões preliminares e foi publicado em periódico em 2019 ([Wiley](https://onlinelibrary.wiley.com/doi/10.1111/obes.12298)); verificar coincidência com o corpus 324.
- Relatórios da Eurofound e documentos de bancos centrais não devem ser classificados automaticamente como artigos de periódico.
- Foi localizado resumo externo de *The “task approach” to labor markets: an overview* ([DOI](https://doi.org/10.1007/s12651-013-0128-z)), além de resumos de trabalhos sobre rotinização italiana e polarização nos EUA.

## Próximas decisões
1. Fixar o critério de tipo documental (artigos de periódico; ou também working papers e relatórios).
2. Conciliar versões duplicadas e anos editoriais com os 324 trabalhos.
3. Avaliar relevância substantiva dos 40 com síntese; disponibilidade de resumo **não garante inclusão**.
4. Resolver os 11 registros da categoria original `VERIFICAR_DUPLICATA`, não incluídos no escopo desta conferência.
5. Somente então congelar uma próxima versão do corpus e executar novamente as análises.

**Rastreabilidade:** planilha Excel, CSVs individualizados, script e relatório detalhado foram fornecidos ao pesquisador no pacote `CONFERENCIA_72_FONTES_49_RESUMOS_17NOV2026.zip`, separado deste repositório. Este documento não representa revisão integral dos PDFs nem validação humana independente de cada obra.
