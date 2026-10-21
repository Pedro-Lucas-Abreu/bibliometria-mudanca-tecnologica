#!/usr/bin/env python3
"""Triagem conservadora/reprodutivel de registros OpenAlex de polarizacao ocupacional.

Fonte: exportacoes das seis consultas do usuario (2000-2025). Metadados, sem texto integral.
As categorias sao provisórias. A validação de 120 títulos/resumos e humana, estratificada,
não equivale à leitura integral dos 3468 registros.
"""
from __future__ import annotations
import csv,json,re,unicodedata,collections,math,random
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
IN=BASE/'dados'/'originais_openalex'
OUT=BASE/'resultados'/'triagem'
OUT.mkdir(exist_ok=True)

def norm(s):
    s=unicodedata.normalize('NFKD',str(s or '').casefold())
    s=''.join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r'[–—‐‑−]','-',s)
    return re.sub(r'\s+',' ',s).strip()

def csv_read(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def csv_write(path,rs,fields):
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rs)

records=csv_read(IN/'01_base_unificada.csv')
raw=json.load(open(IN/'07_openalex_uniao_vosviewer.json',encoding='utf8'))
raw_by_id={x['id']:x for x in raw['results']}
assert len(records)==len(raw_by_id)==3468
assert len({x['openalex_id'] for x in records})==3468

# Títulos: compromisso forte com o objeto específico, incluindo ortografias variantes.
LAB=r'(?:jobs?|employment|occupations?|occupational|labou?r(?:\s+market)?|work(?:force)?|wages?|earnings?|skills?|tasks?)'
POL=r'(?:polari[sz](?:ation|ed|ing)|polaris(?:ation|e|ing)|polarizacion|polarisierung|polarisation)'
TITLE_EXPLICIT=[
    re.compile(r'\b'+LAB+r'\s+(?:market\s+)?'+POL+r'\b',re.I),
    re.compile(r'\b'+POL+r'\s+(?:of|in|among|across|between|within)\s+(?:(?:the|a|us|u\.?s\.?|american|british|european|u\.?k\.?)\s+){0,4}'+LAB+r'\b',re.I),
    re.compile(r'\b'+POL+r'\s+(?:of|in|among|across|between|within)\s+(?:the\s+)?(?:u\.?s\.?\s+)?(?:labou?r\s+market|job\s+opportunities)\b',re.I),
    re.compile(r'\b(?:job(?:s)?|employment|occupation(?:s)?|labor|labour|emploi|empleo|emprego|arbeit|lavoro)\S*\s+polari\w+\b',re.I),
    re.compile(r'\bpolari\w+\s+(?:de|del|des|de l|de la|du|da|do|of)\s+(?:l.emploi|emploi|empleo|emprego|labor|labour|arbeit|work)\b',re.I),
]
TITLE_MECHANISM=re.compile(r'\b(?:routin(?:e|ization|isation)[-\s]*biased|task[-\s]*biased|routinization[-\s]*biased)\s+(?:technical|technological)\s+change\b',re.I)
TITLE_OCCUP_POL=re.compile(r'\b'+POL+r'\b',re.I)
TITLE_EMP=re.compile(r'\b(?:job|jobs|employment|occupational|occupation|labou?r\s+market|routin(?:e|ization|isation)|middle[- ](?:skill|wage)|skill\s+demand|wage\s+distribution)\b',re.I)
ABSTRACT_STRONG=re.compile(r'\b'+LAB+r'\s+(?:market\s+)?'+POL+r'\b|\b'+POL+r'\s+(?:of|in|among|across|between|within)\s+(?:(?:the|a|us|u\.?s\.?|american|british|european)\s+){0,3}'+LAB+r'\b',re.I)
ABSTRACT_MECHANISM=TITLE_MECHANISM
NEG_POL=re.compile(r'\b(?:political|partisan|electoral|ideological|religious|affective|social|geographic|spatial)\s+polari\w+\b',re.I)
NEG_SCI=re.compile(r'\b(?:photonic|photons?|optical|light\s+polarization|electron\s+polarization|spin\s+polarization|fiber\s+polarization|crystal\s+fiber|polarization\s+mode|electromagnetic)\b',re.I)
NEG_REVIEW=re.compile(r'\b(?:book\s+review|review\s+of\s+the\s+book|comment\s+on|erratum|correction\s+to|data\s+for:)\b',re.I)
GOOD_TOPIC=re.compile(r'\b(?:labor market|labour market|employment|digital economy|wage inequality|work transformation|occupational|global trade|migration and labor|gender studies|income, poverty|labor movements|labor law|labor market and education|economic theory)\b',re.I)

# CLASSIFICACOES HISTORICAS DE 120 REGISTROS de trabalho anterior.
# Estao explicitadas abaixo para reproduzir a decisao antiga, mas NAO sao nova auditoria cega
# ou validacao integral da elegibilidade do corpus. Consulte documentacao/02_METODOLOGIA.md.
MANUAL_INCLUDE={
 1,2,3,4,5,6,7,10,12,13,15,16,18,19,21,22,24,26,27,28,29,30,
 33,38,39,40,42,43,47,49,52,53,55,59,
 61,68,69,70,71,73,78,79,80,81,85,88,90,
 95,
}
MANUAL_UNCERTAIN={
 9,20,23,31,32,36,45,46,50,56,57,62,63,64,66,74,76,84,86,89,91,103,
}
MANUAL_EXCLUDE=set(range(1,121))-MANUAL_INCLUDE-MANUAL_UNCERTAIN
assert len(MANUAL_INCLUDE|MANUAL_UNCERTAIN|MANUAL_EXCLUDE)==120
assert not ((MANUAL_INCLUDE & MANUAL_UNCERTAIN) | (MANUAL_INCLUDE & MANUAL_EXCLUDE))
manual=csv_read(BASE/'dados'/'insumos_triagem'/'amostra_120_estratificada.csv')
manual_by_id={r['openalex_id']:('incluir' if i+1 in MANUAL_INCLUDE else 'duvida' if i+1 in MANUAL_UNCERTAIN else 'excluir') for i,r in enumerate(manual)}


def decide(r,j):
    t=norm(r['titulo']);a=norm(r['resumo']);topic=norm(r['topico_primario']);kws=norm(r['palavras_openalex']);area=norm(r['area_topico']);
    loc=j.get('primary_location') or {};src=loc.get('source') or {}
    source_type=src.get('type') or ''
    raw_type=norm(loc.get('raw_type') or '')
    title_direct=any(p.search(t) for p in TITLE_EXPLICIT)
    title_mech=bool(TITLE_MECHANISM.search(t))
    title_generic=bool(TITLE_OCCUP_POL.search(t) and TITLE_EMP.search(t))
    ab_direct=bool(ABSTRACT_STRONG.search(a))
    ab_mech=bool(ABSTRACT_MECHANISM.search(a))
    topic_good=bool(GOOD_TOPIC.search(topic) or 'economics, econometrics' in area)
    keyword_specific=any(k in kws for k in ('job polarization','employment polarization','occupational polarization','labor market polarization','labour market polarization','routine-biased technological change','routine-biased technical change'))
    negative=bool(NEG_SCI.search(t) or (NEG_POL.search(t) and not (title_direct or title_mech)))
    wrongdoc=bool(NEG_REVIEW.search(t) or 'thesis' in raw_type or 'tesi di dottorato' in raw_type or 'dissertation' in raw_type or raw_type=='book-review')
    # Exceptions discovered by auditing top-cited and multilingual titles.
    if re.search(r'\bpolari\w+\s+of\s+(?:the\s+)?(?:u\.?s\.?|us)\s+labou?r\s+market\b',t):title_direct=True
    if re.search(r'\b(?:upgrading\s+or\s+polarization|has\s+ict\s+polarized\s+skill\s+demand)\b',t):title_direct=True
    # E.g. title says occupational shifts / hollowing out and abstract explains polarization.
    if negative: decision,reason='nao_selecionado','polarizacao_nao_ocupacional_ou_termo_fisico'
    elif wrongdoc: decision,reason='revisar','tipo_documental_nao_cientifico_ou_duplicata_potencial'
    elif title_direct and source_type=='journal':decision,reason='nucleo_provisorio','polarizacao_ocupacional_explicita_titulo_e_periodico'
    elif title_mech and source_type=='journal' and topic_good:decision,reason='nucleo_provisorio','mecanismo_tecnologico_explicito_titulo_e_periodico'
    elif title_direct or title_mech:decision,reason='revisar','titulo_relevante_mas_fonte_sem_confirmacao_periodico'
    elif title_generic and topic_good:decision,reason='revisar','titulo_proximo_mas_precisa_confirmar_tipo_de_polarizacao'
    elif ab_direct and topic_good and source_type=='journal':decision,reason='revisar','polarizacao_laboral_no_resumo_sem_foco_explicito_no_titulo'
    elif ab_direct or (ab_mech and topic_good):decision,reason='revisar','resumo_menciona_tema_sem_foco_principal_confirmado'
    elif keyword_specific and topic_good:decision,reason='revisar','keyword_openalex_e_topico_compativeis_nao_suficientes'
    else:decision,reason='nao_selecionado','metadados_sem_evidencia_especifica_de_polarizacao_ocupacional'
    return decision,reason,source_type,raw_type,title_direct,title_mech,ab_direct,topic_good,keyword_specific

all_records=[]
for r in records:
    rid=r['openalex_id'];j=raw_by_id[rid]
    decision,reason,src,rawtype,td,tm,ad,tg,kw=decide(r,j)
    all_records.append({**r,'categoria_triada':decision,'justificativa_regra':reason,'tipo_fonte_openalex':src or 'nao_identificado','tipo_original':rawtype,'ancora_titulo':int(td),'mecanismo_titulo':int(tm),'ancora_resumo':int(ad),'topico_compativel':int(tg),'keyword_especifica':int(kw),'decisao_amostra_120':manual_by_id.get(rid,'')})
counts=collections.Counter(x['categoria_triada'] for x in all_records)
print('AUTOMATIC COUNTS',counts)
print('reason',collections.Counter(x['justificativa_regra'] for x in all_records))

# Examine manual sample vs automation, then assemble reproducible outputs.
manual_out=[]
by_id={x['openalex_id']:x for x in all_records}
for i,r in enumerate(manual,1):
    cat='incluir' if i in MANUAL_INCLUDE else 'duvida' if i in MANUAL_UNCERTAIN else 'excluir'
    a=by_id[r['openalex_id']]
    r.update({'numero_amostra':i,'decisao_titulo_resumo':cat,
       'justificativa_qualitativa':('aborda diretamente estrutura ocupacional, tarefas, mudanca tecnologica ou polarizacao do emprego' if cat=='incluir' else
                                    'tema parcialmente relacionado, sem foco suficientemente claro nos metadados disponíveis' if cat=='duvida' else
                                    'tema fora do objeto definido ou documento de natureza inadequada'),
       'triagem_automatica':a['categoria_triada'],'tipo_fonte_openalex':a['tipo_fonte_openalex']})
    manual_out.append(r)

# Corrections based ONLY on audited 120; preserve distinction from full review.
for r in all_records:
    decision=manual_by_id.get(r['openalex_id'])
    if decision=='incluir' and r['tipo_fonte_openalex']=='journal':
        r['categoria_triada']='nucleo_provisorio';r['justificativa_regra']='revisao_qualitativa_amostra_titulo_resumo'
    elif decision=='excluir':
        r['categoria_triada']='nao_selecionado';r['justificativa_regra']='revisao_qualitativa_amostra_titulo_resumo'
    elif decision=='duvida':
        r['categoria_triada']='revisar';r['justificativa_regra']='revisao_qualitativa_amostra_titulo_resumo'
counts=collections.Counter(x['categoria_triada'] for x in all_records)
print('COUNTS AFTER 120 REVIEW',counts)

# Avoid spurious duplicate journal versions in the screening; flag not auto discard.
normal_title=collections.defaultdict(list)
for r in all_records:
    key=re.sub(r'[^a-z0-9]+','',norm(r['titulo']))
    if len(key)>22:normal_title[key].append(r)
for group in normal_title.values():
    if len(group)>1:
       for x in group:x['suspeita_duplicidade_titulo']='sim'
for x in all_records:x.setdefault('suspeita_duplicidade_titulo','nao')

# Files.
fields=list(records[0])+['categoria_triada','justificativa_regra','tipo_fonte_openalex','tipo_original','ancora_titulo','mecanismo_titulo','ancora_resumo','topico_compativel','keyword_especifica','decisao_amostra_120','suspeita_duplicidade_titulo']
csv_write(OUT/'01_decisoes_3468.csv',all_records,fields)
core=[x for x in all_records if x['categoria_triada']=='nucleo_provisorio']
review=[x for x in all_records if x['categoria_triada']=='revisar']
excluded=[x for x in all_records if x['categoria_triada']=='nao_selecionado']
csv_write(OUT/'02_nucleo_provisorio.csv',core,fields)
csv_write(OUT/'03_revisao_pendente.csv',review,fields)
csv_write(OUT/'04_amostra_120_avaliada.csv',manual_out,list(manual_out[0]))
with (OUT/'05_nucleo_provisorio_openalex.json').open('w',encoding='utf8') as f:
    subset=[raw_by_id[r['openalex_id']] for r in core]
    json.dump({'meta':{'count':len(subset),'per_page':len(subset),'source':'nucleo_provisorio_seis_buscas_2000_2025_triagem_versao_1'},'results':subset},f,ensure_ascii=False)

summary=[]
for group,sub in [('universo',all_records),('nucleo_provisorio',core),('revisar',review),('nao_selecionado',excluded)]:
    summary.append({'grupo':group,'n':len(sub),'fonte_periodico':sum(x['tipo_fonte_openalex']=='journal' for x in sub),
       'sem_referencias':sum(int(x['n_referencias'] or 0)==0 for x in sub),
       'sem_resumo':sum(not (x['resumo'] or '').strip() for x in sub),
       'sem_pais':sum(not (x['paises'] or '').strip() for x in sub),
       'duplicidade_titulo_potencial':sum(x['suspeita_duplicidade_titulo']=='sim' for x in sub),
       'citado_mais_100':sum(int(x['citacoes'] or 0)>=100 for x in sub)})
csv_write(OUT/'06_cobertura_e_qualidade.csv',summary,list(summary[0]))

# Selected corpus yearly counts, cautiously descriptive conditional on this screen.
year_counts=collections.Counter(x['ano'] for x in core)
csv_write(OUT/'07_ano_nucleo_provisorio.csv',[{'ano':y,'n':year_counts.get(str(y),0)} for y in range(2000,2026)],['ano','n'])

# List of leading works in core and review, independently of keyword score.
top=[]
for group,data in [('nucleo_provisorio',core),('revisar',review)]:
    for r in sorted(data,key=lambda x:-int(x['citacoes'] or 0))[:55]:
        top.append({'grupo':group,'openalex_id':r['openalex_id'],'titulo':r['titulo'],'ano':r['ano'],
                    'citacoes':r['citacoes'],'tipo_fonte':r['tipo_fonte_openalex'],'motivo':r['justificativa_regra']})
csv_write(OUT/'08_mais_citados_para_conferencia.csv',top,list(top[0]))

mcounts=collections.defaultdict(collections.Counter)
for r in manual_out:mcounts[r['classe_triagem']][r['decisao_titulo_resumo']]+=1
csv_write(OUT/'09_validacao_amostral_por_regra.csv',[
    {'classe_regra_original':k,'incluir':n['incluir'],'duvida':n['duvida'],'excluir':n['excluir'],
     'total':sum(n.values())} for k,n in sorted(mcounts.items())],
    ['classe_regra_original','incluir','duvida','excluir','total'])

# Save result notes; no citation references from sources elsewhere are implied.
report=f'''# Triagem do corpus OpenAlex — polarizacao ocupacional (2000–2025)

## O que foi realizado

- Fonte: seis consultas OpenAlex `title_abstract_keywords`, selecionando `type:article` e 2000–2025; base congelada enviada pelo usuário.
- Populacao inicial: **{len(all_records):,} registros unicos OpenAlex** (4.975 aparições nas seis buscas).
- Triagem de **todos os registros** por regras explícitas em título, resumo, campo e tipo de fonte.
- **120 registros amostrados foram examinados pelo título e trecho de resumo disponível**; não lemos o texto integral.
- Três saídas separadas: núcleo conservador **{len(core):,}**, revisão pendente **{len(review):,}**, não selecionados automaticamente **{len(excluded):,}**.

**O núcleo é PROVISÓRIO, não uma revisão sistemática definitiva:** a triagem automática não foi confirmada manualmente linha por linha, e existem documentos sem resumo, em outras línguas e erros de indexação.

## Regra econômica de inclusão

Incluem-se pesquisas sobre: mudanças relativas na participação de ocupações/empregos de baixa, média e alta remuneração ou qualificação (polarização, upgrading, hollowing out); mudança tecnológica baseada em tarefas/rotinização como explicação desses padrões; e evidência ocupacional relacionada a salários e desigualdade. A simples menção incidental a empregos, desigualdade ou IA não basta.

A classe **núcleo provisório** privilegia artigos de periódicos cujos títulos contêm o fenômeno estudado ou os mecanismos diretamente associados; alguns registros da amostra estratificada foram corrigidos qualitativamente.

**Revisar** significa que um documento potencialmente pertinente exige leitura mais atenta, ou sua fonte não confirma publicação em periódico. **Não selecionado** significa que as informações de busca e metadados não demonstram pertinência suficiente para o núcleo; não é uma sentença de irrelevância teórica.

## Auditoria do corpus

| Grupo | N | Artigos em periódicos | Sem referências indexadas | Sem país afiliado | Sem resumo | Títulos possivelmente duplicados |
|---|---:|---:|---:|---:|---:|---:|
'''
for x in summary:report+=f"| {x['grupo']} | {x['n']:,} | {x['fonte_periodico']:,} | {x['sem_referencias']:,} | {x['sem_pais']:,} | {x['sem_resumo']:,} | {x['duplicidade_titulo_potencial']:,} |\n"
report+='''

### Validação amostral estratificada

'''
report+='| Regra original | Incluir | Dúvida | Excluir | Total |\n|---|---:|---:|---:|---:|\n'
for k,n in sorted(mcounts.items()):report+=f"| {k} | {n['incluir']} | {n['duvida']} | {n['excluir']} | {sum(n.values())} |\n"
report+='''

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
'''
(OUT/'00_RELATORIO_TRIAGEM.md').write_text(report,encoding='utf-8')
print('WORKS',len(all_records),'CORE',len(core),'REVIEW',len(review),'NOT_SELECTED',len(excluded))
print('MANUAL',dict((k,dict(v)) for k,v in mcounts.items()))
print('OUTPUT',OUT)
