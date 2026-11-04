# Mudança tecnológica, polarização ocupacional e desigualdade salarial (2000–2025)

Repositório de **dados, código e resultados** de uma análise bibliométrica exploratória da literatura sobre mudança tecnológica e polarização ocupacional. Projeto acadêmico da disciplina de doutorado em Economia da UFSC.

**Situação em 03/11/2026:** a base inicial contém **3.468 registros únicos** extraídos do OpenAlex por seis consultas. A triagem automatizada e uma amostra manual de títulos/resumos produziram **208 artigos em núcleo provisório**, **845 pendentes de avaliação** e **2.415 não selecionados**. **O corpus não foi validado integralmente.** As redes e figuras são descritivas e condicionais ao processo de busca e seleção; não representam toda a literatura nem identificam efeitos causais.

**O manuscrito em LaTeX e seu PDF são mantidos fora deste repositório.** Este espaço disponibiliza a base processada e o código de reprodução, não o texto do artigo.

## Estrutura

- `dados/originais_openalex/`: exportação congelada e auditoria das consultas do OpenAlex.
- `dados/insumos_triagem/`: insumos para a triagem e a amostra de 120 registros examinados por título/resumo.
- `scripts/`: validação, regras de triagem, redes bibliométricas, testes, rastreabilidade, relatório e evolução de palavras-chave.
- `resultados/triagem/`: decisões para o universo de 3.468 registros, núcleo provisório de 208 e casos pendentes.
- `resultados/analises/`: tabelas, indicadores e figuras de redes e evolução temática.
- `resultados/rastreabilidade/`: documentos e referências que sustentam as ligações representadas.
- `documentacao/02_METODOLOGIA.md`: critérios, parâmetros, fórmulas e limitações.
- `documentacao/04_PENDENCIAS.md`: questões científicas que permanecem sem resolução.
- `resultados/RELATORIO_REPRODUZIVEL.md`: relatório das análises originais.

## Como reproduzir (Python 3.11+)

Execute na raiz do repositório:

```powershell
python -m pip install -r requirements.txt
python executar_tudo.py
```

As análises utilizam arquivos locais congelados, sem requerer chave de API nem nova consulta ao OpenAlex. O fluxo executa nove scripts, incluindo `scripts/09_evolucao_keywords.py`, que reproduz a evolução temática em janelas móveis de cinco anos.

**Gráfico temporal adicionado em 03/11/2026:**
- [Tabela com os numeradores, denominadores e percentuais](resultados/analises/evolucao_keywords_janelas_5anos.csv).
- [Código que reproduz a tabela e o PNG da figura](scripts/09_evolucao_keywords.py).

O gráfico mede o percentual de documentos com determinadas palavras-chave atribuídas pelo OpenAlex; não estima modelos dinâmicos de tópicos (DTM), LDA ou STM. Cada ponto usa uma janela de cinco anos e somente janelas com pelo menos 20 documentos são mostradas. As janelas se sobrepõem e não constituem observações independentes.

Para conferir a execução, consulte `resultados/resumo_reproducibilidade.json`, `resultados/analises/indicadores.json` e `resultados/RELATORIO_REPRODUZIVEL.md`. O arquivo `resultados/analises/fig3_evolucao_janelas_5anos.png` é gerado localmente após a execução completa.

## Acesso aos dados processados

- [Núcleo provisório (208 registros)](resultados/triagem/02_nucleo_provisorio.csv)
- [Classificação dos 3.468 registros](resultados/triagem/01_decisoes_3468.csv)
- [Revisão pendente (845 registros)](resultados/triagem/03_revisao_pendente.csv)
- [Resultados bibliométricos](resultados/analises/)
- [Rastreabilidade das redes](resultados/rastreabilidade/)

URL pública: https://github.com/Pedro-Lucas-Abreu/bibliometria-mudanca-tecnologica

## Alcance e limitações

As decisões automáticas dependem de títulos, resumos e metadados de indexação; 120 registros foram examinados apenas por título e trecho de resumo, sem leitura integral. Há potenciais duplicatas e ausências de trabalhos centrais. Parte dos registros não tem referências indexadas nem país de afiliação identificado. As consultas originais privilegiam polarização ocupacional e RBTC; não cobrem de maneira abrangente inteligência artificial nem transição verde/digital.

Os resultados publicados são **exploratórios**. A reprodução computacional não substitui a validação substantiva da seleção; ver [metodologia](documentacao/02_METODOLOGIA.md) e [pendências](documentacao/04_PENDENCIAS.md).

Metadados bibliográficos: OpenAlex. O repositório não distribui textos integrais de artigos protegidos por direitos autorais.
