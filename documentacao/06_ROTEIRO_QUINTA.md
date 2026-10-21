# GUIA DE REUNIÃO COM DOMINIK — quinta-feira, 22/10/2026

## Abertura sugerida (45–60 segundos)

“Professor, decidi concentrar o trabalho da disciplina na bibliometria, com uma revisão narrativa que conecte a literatura de polarização ocupacional às discussões atuais de inteligência artificial e transição verde/digital, como o senhor sugeriu. Já reuni seis consultas do OpenAlex, eliminei duplicações por ID e programei redes de palavras-chave, acoplamento bibliográfico e indicadores temporais. Tenho 3.468 registros únicos e um núcleo provisório de 208, ainda sujeito a auditoria. Trouxe os resultados exploratórios, as limitações e um esqueleto do artigo para discutirmos o recorte antes de finalizar.”

## Roteiro de 7–9 minutos

1. **Pergunta econômica (1 min).** Estrutura da literatura sobre polarização, tarefas e desigualdade; IA/verde como agenda recente, ainda sem cobertura bibliométrica suficiente.
2. **Protocolo de coleta e triagem (1,5 min).** Seis buscas -> 4.975 ocorrências -> 3.468 IDs -> 208 provisórios, 845 pendentes. Mostrar planilha de decisões por documento.
3. **Mapa temático (1,5 min).** 56 termos, 545 arestas, cinco comunidades, modularidade 0,1371. Não atribuir significado causal aos clusters.
4. **Evolução (1 min).** Keywords `automation`: 0/28, 6/71, 14/109 por períodos. Interpretar como proporção entre documentos recuperados e indexados.
5. **Acoplamento e colaboração (1,5 min).** 162 documentos com refs; ligações por referências comuns; 165 documentos com país identificado; mostrar arquivo que identifica as fontes de uma aresta.
6. **Revisão de literatura e extensão (1 min).** Tarefas e rotinização -> automação -> IA; demanda por competências na transição verde/digital. Esta etapa é narrativa até definir uma nova coleta.
7. **Dúvidas substantivas (1 min).** Pedir orientação sobre delimitação e critérios para a seleção final e a integração da revisão recente.

## Arquivos para deixar abertos no VS Code

- `resultados/RELATORIO_REPRODUZIVEL.md` (Ctrl+Shift+V para pré-visualização).
- `resultados/analises/fig2_rede_keywords.png` e `resultados/analises/fig3_temas_por_periodo.png`.
- `resultados/analises/fig5_acoplamento_normalizado_k5.png`.
- `resultados/triagem/01_decisoes_3468.csv`.
- `scripts/02_triagem.py` e `scripts/03_redes_e_figuras.py`.
- `documentacao/05_ESQUELETO_ARTIGO.md`.

## Perguntas prováveis e respostas curtas

**Por que 208?** “É um núcleo conservador automatizado com regras explícitas, não o universo final validado. Ainda preciso auditar a inclusão e avaliar os 845 pendentes.”

**Como sabe que há cinco escolas científicas?** “Não afirmo isso. O algoritmo detectou cinco comunidades de keywords nas condições escolhidas, e modularidade relativamente baixa indica sobreposição; a interpretação substantiva ainda depende da leitura.”

**Onde está a cocitação?** “O que está calculado de modo rastreável é coocorrência e acoplamento bibliográfico. Cocitação fica como possível extensão.”

**IA e verde já estão nas redes?** “A amostra inicial não foi desenhada para representar adequadamente esses eixos. Vou incluí-los na revisão narrativa e, se forem o objeto quantitativo central, refazer buscas com protocolo registrado.”

**O artigo está pronto?** “O pipeline é reproduzível e gera resultados exploratórios. A seleção e a discussão teórica ainda estão em desenvolvimento.”

**Por que há diferença entre a modularidade no PDF anterior e no relatório?** “São resultados de execuções/documentos de fases diferentes: 0,1345 no arquivo anterior e 0,1371 na execução reprodutível mais recente. Vou comparar configurações e dependências antes de escolher a versão final e evitar misturá-las.”

## Cuidados

- O PDF `material_bibliometria_para_quinta` é uma apresentação **mais antiga**: sua modularidade mínima 5 aparece como **0,1345 ≈ 0,135**, enquanto o relatório reproduzível usa **0,1371**. Não citar os dois como se fossem exatamente o mesmo cálculo.
- Há uma rede antiga do VOSviewer com **150 nós**, distinta da rede reproduzida do corpus de 208 com **56 nós**. Não confundi-las.
- Palavras-chave do OpenAlex não equivalem à leitura integral dos artigos.
- **Não** anunciar uma rede de cocitação pronta.

## O que perguntar ao professor

“Para esta disciplina, o senhor preferiria uma bibliometria com revisão narrativa concentrada em IA e transição verde/digital, ou acha importante que eu amplie já o corpus para medir esses eixos quantitativamente? Gostaria de alinhar o escopo antes de fechar o protocolo e a redação.”
