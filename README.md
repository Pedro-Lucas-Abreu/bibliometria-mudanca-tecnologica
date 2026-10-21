# Mudança tecnológica, polarização ocupacional e desigualdade salarial (2000–2025)

Material de pesquisa da disciplina de doutorado em Economia (UFSC): artigo em LaTeX, metadados bibliográficos OpenAlex, código Python, regras de triagem, análises de redes e resultados reproduzíveis.

> **Situação em 21/10/2026: rascunho exploratório.** Os 208 documentos selecionados pertencem a um **núcleo provisório**. Há **845 registros pendentes de revisão**. As figuras não devem ser interpretadas como resultados bibliométricos definitivos, representativos da literatura total, nem como inferência causal.

## Estrutura

- [`artigo/artigo.tex`](artigo/artigo.tex) — manuscrito (2.000–2.500 palavras, versão preliminar), [`referencias.bib`](artigo/referencias.bib), figuras e [`PDF`](artigo/artigo.pdf).
- [`dados/originais_openalex`](dados/originais_openalex) — exportações congeladas do OpenAlex, inclusive JSON original e CSV da coleta.
- [`dados/insumos_triagem`](dados/insumos_triagem) — insumo de triagem.
- [`scripts`](scripts) — oito scripts de validação, triagem, redes, testes, rastreabilidade e relatório.
- [`resultados/triagem`](resultados/triagem) — decisões documentadas para 3.468 registros; lista provisória de 208 e 845 pendentes.
- [`resultados/analises`](resultados/analises) — tabelas, figuras e indicadores.
- [`resultados/rastreabilidade`](resultados/rastreabilidade) — tabelas relacionando redes aos documentos e referências.
- [`documentacao`](documentacao) — metodologia, limitações e roteiro da apresentação.
- [`resultados/RELATORIO_REPRODUZIVEL.md`](resultados/RELATORIO_REPRODUZIVEL.md) — relatório automático.

## Reproduzir os resultados (Python 3.11+)

No terminal, **na raiz do repositório**:

```powershell
python -m pip install -r requirements.txt
python executar_tudo.py
```

O processo utiliza a exportação congelada, sem exigir chave de API ou consulta ativa ao OpenAlex. Após rodar, confira `resultados/resumo_reproducibilidade.json`, `resultados/analises/indicadores.json` e `resultados/RELATORIO_REPRODUZIVEL.md`. Para detalhes dos filtros e métodos, ver [`documentacao/02_METODOLOGIA.md`](documentacao/02_METODOLOGIA.md).

## Compilar o artigo

Dentro de `artigo/`, mantendo `referencias.bib` na mesma pasta:

```powershell
pdflatex artigo.tex
bibtex artigo
pdflatex artigo.tex
pdflatex artigo.tex
```

Alternativamente, use `latexmk -pdf artigo.tex` se estiver instalado. O PDF versionado é uma prévia; quando a triagem for finalizada, recalcule tabelas e figuras antes de revisar o artigo. As figuras do artigo são **cópias congeladas**, não são atualizadas automaticamente ao reexecutar o Python; copie os novos PNGs de `resultados/analises/` para `artigo/figuras/` após a validação.

## Dados processados e citação

- **Base de seleção provisória:** [`resultados/triagem/02_nucleo_provisorio.csv`](resultados/triagem/02_nucleo_provisorio.csv)
- **Classificação de todos os registros:** [`resultados/triagem/01_decisoes_3468.csv`](resultados/triagem/01_decisoes_3468.csv)
- **Pendências de seleção:** [`resultados/triagem/03_revisao_pendente.csv`](resultados/triagem/03_revisao_pendente.csv)
- **Resultados finais da execução:** [`resultados/analises/`](resultados/analises)

Após publicar, o link do repositório será `https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO` (substituir por URL real). **Não trate o link acima como publicado nem o corpus como auditado.**

Os dados de metadados são provenientes do OpenAlex; análises e triagem são trabalhos derivados. As fontes e referências precisam ser conferidas antes da submissão. Não foram incluídos textos integrais de artigos protegidos por direitos autorais.

## Antes da entrega (03/11/2026)

- [ ] Revisar seleção de documentos, duplicatas e 845 casos pendentes segundo protocolo explícito.
- [ ] Reexecutar análises e atualizar PNGs do artigo e números do texto.
- [ ] Ler e conferir pessoalmente ao menos dez referências bibliográficas.
- [ ] Inserir o endereço **real** deste repositório no campo de disponibilização de dados do artigo.
- [ ] Conferir declaração de uso de IA, contagem de palavras e consistência dos resultados.
