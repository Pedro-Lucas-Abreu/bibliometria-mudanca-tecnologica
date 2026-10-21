#!/usr/bin/env python3
"""Rastreabilidade dos indicadores: cada ligação aponta para os IDs-fonte.
Lê o núcleo recriado pela triagem, produz CSVs e GraphML; nenhuma chamada à API.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from math import sqrt
import csv,json,networkx as nx
R=Path(__file__).resolve().parents[1];I=R/'resultados/triagem';O=R/'resultados/rastreabilidade';O.mkdir(parents=True,exist_ok=True)
recs=json.loads((I/'05_nucleo_provisorio_openalex.json').read_text(encoding='utf8'))['results']
byid={x['id']:x for x in recs}
ALIAS={
 'routine-biased technical change':'routine-biased technological change',
 'labour market polarization':'labor market polarization',
 'occupational polarisation':'occupational polarization',
 'job polarisation':'job polarization',
 'labour market':'labor market',
 'technological unemployment':'technology-induced unemployment',
}
def keywords(x):
 return {ALIAS.get(k['display_name'].strip().lower(),k['display_name'].strip().lower()) for k in (x.get('keywords') or []) if k.get('display_name')}
def write(name,fields,rows):
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
terms={o['id']:keywords(o) for o in recs}
freq=Counter(k for ks in terms.values() for k in ks)
selected={t for t,v in freq.items() if v>=5}
# Documento -> keyword (inclui os termos raros para mostrar a origem das frequências)
term_docs=defaultdict(list)
for id,ts in terms.items():
 for t in ts:term_docs[t].append(id)
write('01_keywords_artigos.csv',['keyword','ocorrencias','artigos_openalex_ids'],[
 {'keyword':k,'ocorrencias':len(ids),'artigos_openalex_ids':' | '.join(sorted(ids))} for k,ids in sorted(term_docs.items())])
# Palavra-chave por artigo, com scores originalmente indexados (se existir).
rows=[]
for r in recs:
 for kw in r.get('keywords') or []:
  name=kw.get('display_name','').strip().lower()
  if name:
   rows.append({'openalex_id':r['id'],'ano':r['publication_year'],'keyword_original':name,
                'keyword_harmonizada':ALIAS.get(name,name),'score_openalex':kw.get('score')})
write('02_keyword_atribuicao_documento.csv',['openalex_id','ano','keyword_original','keyword_harmonizada','score_openalex'],rows)
# Coocorrência: os documentos que geram cada ligação, sem pesos inventados.
links=defaultdict(list)
for id,ts in terms.items():
 for a,b in combinations(sorted(ts & selected),2):links[(a,b)].append(id)
kw_g=nx.Graph()
for t in sorted(selected):kw_g.add_node(t,ocorrencias=freq[t])
for (a,b),ids in sorted(links.items()):kw_g.add_edge(a,b,weight=len(ids),documentos_ids=' | '.join(sorted(ids)))
assert kw_g.number_of_nodes()==56 and kw_g.number_of_edges()==545
write('03_arestas_keyword_com_documentos.csv',['keyword_1','keyword_2','peso_coocorrencia','artigos_openalex_ids'],[
 {'keyword_1':a,'keyword_2':b,'peso_coocorrencia':len(ids),'artigos_openalex_ids':' | '.join(sorted(ids))} for (a,b),ids in sorted(links.items())])
nx.write_graphml(kw_g,O/'rede_keywords_56.graphml')
# Bibliographic coupling: listas de IDs de referências COMPARTILHADAS.
refs={id:set(v.get('referenced_works') or []) for id,v in byid.items()}
r_docs=defaultdict(list)
for id,rr in refs.items():
 for ref in rr:r_docs[ref].append(id)
shared=defaultdict(list)
for ref,docs in r_docs.items():
 for a,b in combinations(sorted(docs),2):shared[(a,b)].append(ref)
cp_rows=[]
bib_g=nx.Graph();bib_g.add_nodes_from([id for id in byid if refs[id]])
for (a,b),ref_ids in sorted(shared.items()):
 if len(ref_ids)<2:continue
 ref_ids=sorted(ref_ids)
 weight=len(ref_ids);salton=weight/sqrt(len(refs[a])*len(refs[b]))
 bib_g.add_edge(a,b,weight=weight,salton=salton,referencias_ids=' | '.join(ref_ids))
 cp_rows.append({'artigo_1':a,'titulo_1':byid[a]['display_name'],'artigo_2':b,'titulo_2':byid[b]['display_name'],
                 'n_referencias_compartilhadas':weight,'salton':round(salton,6),'referencias_openalex_ids':' | '.join(ref_ids)})
write('04_arestas_acoplamento_com_referencias.csv',['artigo_1','titulo_1','artigo_2','titulo_2','n_referencias_compartilhadas','salton','referencias_openalex_ids'],cp_rows)
nx.write_graphml(bib_g,O/'rede_acoplamento_peso_min2.graphml')
# País = afiliação institucional, não nacionalidade individual dos pesquisadores.
collab=defaultdict(list)
for obj in recs:
 countries=sorted({c for a in obj.get('authorships') or [] for c in a.get('countries') or [] if c})
 for x,y in combinations(countries,2):collab[(x,y)].append(obj['id'])
write('05_colaboracao_paises_com_artigos.csv',['pais_1','pais_2','n_artigos','artigos_openalex_ids'],[
 {'pais_1':a,'pais_2':b,'n_artigos':len(ids),'artigos_openalex_ids':' | '.join(sorted(ids))} for (a,b),ids in sorted(collab.items())])
# Lista de documentos: perguntas sobre a contribuição -> abrir título, ID, lista de refs e palavras-chave
write('06_artigos_nucleo_e_metadados.csv',['openalex_id','ano','titulo','n_keywords','n_referencias','n_citacoes_openalex','keyword_harmonizada','referencias_ids'],[
 {'openalex_id':x['id'],'ano':x['publication_year'],'titulo':x['display_name'],'n_keywords':len(terms[x['id']]),'n_referencias':len(refs[x['id']]),
  'n_citacoes_openalex':x.get('cited_by_count',0),'keyword_harmonizada':' | '.join(sorted(terms[x['id']])),
  'referencias_ids':' | '.join(sorted(refs[x['id']]))} for x in recs])
summary={'registros_no_nucleo':len(recs),'keywords_todas':len(freq),'keywords_min5':kw_g.number_of_nodes(),'coocorrencias_min5':kw_g.number_of_edges(),'arestas_acoplamento_min2':bib_g.number_of_edges(),'paises_pares':len(collab),'explicacao':'Cada linha de ligação inclui IDs de artigos ou referências exatas que justificam o peso da aresta.'}
(O/'LEIA_ESSES_DADOS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('RASTREABILIDADE PRONTA —',summary)
