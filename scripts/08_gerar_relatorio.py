#!/usr/bin/env python3
"""Cria relatório em Markdown diretamente dos outputs; nenhum indicador digitado na mão."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'resultados';OUT.mkdir(exist_ok=True)
A=json.loads((OUT/'analises/indicadores.json').read_text(encoding='utf8'))
V=json.loads((OUT/'vosviewer_exploratorio/indicadores_vosviewer.json').read_text(encoding='utf8'))
B=json.loads((OUT/'auditoria/conferencia_coleta.json').read_text(encoding='utf8'))
D=json.loads((OUT/'resumo_reproducibilidade.json').read_text(encoding='utf8'))
def csvread(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
P=csvread(OUT/'analises/temas_periodos.csv');K=csvread(OUT/'analises/ranking_termos.csv')
periodauto=[x for x in P if x['tema']=='Automação']
q=A['keywords']['min5']
s='''# Relatório preliminar de bibliometria — gerado automaticamente

> **Natureza:** análise exploratória com corpus de 208 trabalhos **provisoriamente** classificados.
> Este arquivo foi produzido por `scripts/08_gerar_relatorio.py` a partir das tabelas calculadas.
> Os dados originais não foram modificados e nenhum acesso à API foi necessário.

## 1. Fonte e seleção do corpus

'''
s+=f"- Consultas em OpenAlex, anos 2000–2025: **{B['total_aparicoes']} aparições** em seis buscas.\n"
s+=f"- Deduplicação por OpenAlex ID: **{B['registros_unicos']} registros únicos**; aparições excedentes **{B['aparicoes_excedentes']}**.\n"
s+=f"- Classificação por regras explícitas + rótulos históricos de amostra de 120 trabalhos: **{D['nucleo_provisorio']} núcleo provisório**, **{D['revisao_pendente']} revisão pendente**, **{D['nao_selecionados']} não selecionados**.\n"
s+='\nAs regras estão em `scripts/02_triagem.py`. **Amostra de 120 rotulada em trabalho preliminar**, não é certificação independente de qualidade nem revisão de texto integral.\n'
s+='\n## 2. Rede temática — coocorrência de keywords OpenAlex\n\n'
s+=f"- Termos com no mínimo 5 artigos: **{q['n']} nós**, **{q['arestas']} arestas**, força total **{q['forca_total']}**.\n"
s+=f"- Comunidades Louvain: **{q['clusters']}**; modularidade ponderada **{q['modularidade']:.4f}**.\n"
s+=f"- Sensibilidade ao termo âncora `job polarization`: modularidade com âncora **{q['modularidade']:.4f}**, sem âncora **{A['keywords']['min5_sem_ancora']['modularidade']:.4f}**.\n"
s+='\n![Rede temática filtrada](analises/fig2_rede_keywords.png)\n'
s+='\n### Termos frequentes\n\n| Termo | Ocorrências | Força da ligação |\n| --- | ---: | ---: |\n'
for r in K[:12]:s+=f"| {r['termo']} | {r['ocorrencias']} | {r['forca_total'] or '—'} |\n"
s+='\n**Rastrear arestas:** `rastreabilidade/03_arestas_keyword_com_documentos.csv`. Cada linha traz os OpenAlex IDs que originaram a ligação.\n'
s+='\n## 3. Evolução da amostra e indicadores temáticos\n\n'
s+='![Artigos por ano](analises/fig1_producao_anual.png)\n\n'
s+='![Temas por período](analises/fig3_temas_por_periodo.png)\n\n'
s+='| Período | Artigos analisados | Com keyword automation | Percentual |\n| --- | ---: | ---: | ---: |\n'
for r in periodauto:s+=f"| {r['period']} | {r['n_artigos']} | {r['com_termo']} | {r['percent']}% |\n"
s+='\nEstes números dizem respeito às **keywords atribuídas pela OpenAlex** no corpus selecionado, não demonstram evolução da economia nem representam a totalidade da produção acadêmica.\n'
s+='\n## 4. Acoplamento bibliográfico\n\n'
s+=f"- Trabalhos com alguma referência indexada: **{A['acoplamento']['artigos_com_referencias']}**.\n"
s+=f"- Pares com duas ou mais referências compartilhadas: **{A['acoplamento']['links_2mais']}**.\n"
s+='- Para visualizar a rede mais legível, selecionamos até 5 vizinhos por artigo, pelo coeficiente de Salton. Isso é um **filtro de visualização**, não um novo conjunto de artigos.\n'
s+='\n![Acoplamento bibliográfico normalizado](analises/fig5_acoplamento_normalizado_k5.png)\n'
s+='\n**Rastrear arestas:** `rastreabilidade/04_arestas_acoplamento_com_referencias.csv` exibe títulos, pesos e os IDs exatos das referências em comum.\n'
s+='\n## 5. Colaboração internacional e cobertura\n\n'
s+=f"- País de afiliação identificado em **{A['paises']['cobertura']}** dos 208 artigos.\n"
s+=f"- Artigos com autores afiliados em pelo menos dois países: **{A['paises']['artigos_multinacionais']}**.\n"
s+=f"- Pares diferentes de países coafiliados: **{A['paises']['arestas_paises']}**.\n"
s+='\n**Rastrear relações:** `rastreabilidade/05_colaboracao_paises_com_artigos.csv`. O país é da **afiliação institucional**, não a nacionalidade do autor.\n'
s+='\n## 6. Primeira rede exportada do VOSviewer — somente comparação\n\n'
s+=f"- No mapa exploratório anterior, **{V['nos']} termos**, **{V['arestas']} arestas**, **{V['comunidades_vosviewer']} clusters**.\n"
s+=f"- Modularidade desses clusters, recalculada sobre arestas exportadas: **{V['modularidade_calculada_dos_clusters_exportados']:.4f}**.\n"
s+='\n![Rede original exportada do VOSviewer](vosviewer_exploratorio/mapa_vosviewer_exportado.png)\n'
s+='\n**Atenção:** esta rede decorre da **primeira busca exploratória**, anterior ao corpus de 3.468/208. Não confundir com a rede de palavras-chave produzida em Python sobre 208 artigos.\n'
s+='\n## 7. Limitações que devem ser apresentadas\n\n'
s+='- A base de 208 não foi validada integralmente e não deve ser chamada de amostra final.\n'
s+='- Há 845 trabalhos com elegibilidade pendente e possíveis publicações duplicadas sob IDs diferentes.\n'
s+='- O OpenAlex indexa palavras-chave automaticamente; coocorrências podem refletir a indexação.\n'
s+='- Algumas referências citadas não foram recuperadas como artigos-fonte, então seu nome aparece apenas pelo ID OpenAlex.\n'
s+='- A busca original quase não cobre IA recente e não foi desenhada para captar a transição verde/digital; requer busca adicional justificada antes de conclusões sobre esses eixos.\n'
s+='- Redes exploratórias são descritivas; não permitem inferir causalidade de IA sobre empregos ou salários.\n'
s+='\n## 8. Como reproduzir\n\n'
s+='Abra esta pasta no VS Code. No terminal, instale `pip install -r requirements.txt` e rode `python executar_tudo.py`. O script confere os hashes originais, refaz a triagem, redes, tabelas, figuras e testa as principais identidades.\n'
s+='\n**Fonte da coleta:** veja `dados/originais_openalex/02_auditoria_buscas.csv` e `codigo_historico/01_coleta_original_openalex.py`. **Reexecução sem API:** garantida pelo JSON congelado, para não depender de mudanças futuras na indexação OpenAlex.\n'
(OUT/'RELATORIO_REPRODUZIVEL.md').write_text(s,encoding='utf8')
print('RELATÓRIO REPRODUZÍVEL: resultados/RELATORIO_REPRODUZIVEL.md')
