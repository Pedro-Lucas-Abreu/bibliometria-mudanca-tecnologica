"""Analise bibliometrica preliminar reproduzivel; base congelada OpenAlex (out/2026).
Requer: pandas, matplotlib, networkx. Resultados NAO equivalem a corpus validado.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter, defaultdict
import json, csv, re, math, statistics
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'resultados' / 'analises'
OUT.mkdir(exist_ok=True)
D = pd.read_csv(BASE/'resultados/triagem/02_nucleo_provisorio.csv',sep=';',keep_default_na=True)
RAW = json.load(open(BASE/'resultados/triagem/05_nucleo_provisorio_openalex.json', encoding='utf8'))['results']
byid={v['id']:v for v in RAW}
R=[byid[x] for x in D.openalex_id if x in byid]
assert len(R)==len(D)==208

# Minimal transparent harmonization: singular English variants of the same named construct.
ALIAS={
 'routine-biased technical change':'routine-biased technological change',
 'labour market polarization':'labor market polarization',
 'occupational polarisation':'occupational polarization',
 'job polarisation':'job polarization',
 'labour market':'labor market',
 'technological unemployment':'technology-induced unemployment',
}
def kws(obj):
    return sorted({ALIAS.get(x['display_name'].strip().lower(), x['display_name'].strip().lower()) for x in (obj.get('keywords') or []) if x.get('display_name')})
terms_by_id={v['id']:kws(v) for v in R}
frequency=Counter(t for terms in terms_by_id.values() for t in terms)

def keyword_network(minfreq=5, remove_anchor=False):
    selected={t for t,n in frequency.items() if n>=minfreq and (not remove_anchor or t!='job polarization')}
    g=nx.Graph()
    for t in sorted(selected):g.add_node(t,occ=frequency[t])
    for obj in R:
        these=sorted(set(terms_by_id[obj['id']]) & selected)
        for a,b in combinations(these,2):
            if g.has_edge(a,b):g[a][b]['weight']+=1
            else:g.add_edge(a,b,weight=1)
    return g

def detect(g, seed=42):
    return list(nx.community.louvain_communities(g,weight='weight',seed=seed,resolution=1.0))

def metrics(g):
    cc=detect(g)
    w_tot=sum(e['weight'] for _,_,e in g.edges(data=True))
    win=sum(g[a][b]['weight'] for C in cc for a,b in combinations(C,2) if g.has_edge(a,b))
    return dict(n=g.number_of_nodes(),edges=g.number_of_edges(),sum_weights=w_tot,components=nx.number_connected_components(g),clusters=len(cc),modularity=nx.community.modularity(g,cc,weight='weight'),cross_weight_share=(w_tot-win)/w_tot if w_tot else None,partitions=cc)

G=keyword_network(5); M=metrics(G)
G_no=keyword_network(5,True); M_no=metrics(G_no)
M3=metrics(keyword_network(3)); M8=metrics(keyword_network(8))
central=nx.betweenness_centrality(G,normalized=True,weight=None)
strength=dict(G.degree(weight='weight'))
cs=sorted(M['partitions'],key=len,reverse=True)
cluster_rows=[]
for i,C in enumerate(cs,1):
  top=sorted(C,key=lambda t:(strength[t],frequency[t]),reverse=True)[:8]
  cluster_rows.append(dict(cluster=i,n=len(C),terms=', '.join(top[:7]),strength=sum(strength[t] for t in C)))

# time slices: publish years; report term shares, NOT change in economic impact.
periods=[('2000–2012',2000,2012),('2013–2018',2013,2018),('2019–2025',2019,2025)]
termsets={
 'Polarização ocupacional':{'job polarization','labor market polarization','occupational polarization','employment polarization'},
 'Rotinização / RBTC':{'routine-biased technological change','routine tasks','routine occupations','routine-biased technical change'},
 'Automação':{'automation','robotics','industrial robots'},
 'Inteligência artificial':{'artificial intelligence','generative artificial intelligence','generative ai','machine learning','ai technology'},
 'Offshoring':{'offshoring'},
 'Desigualdade salarial':{'wage inequality','wage polarization','wage distribution'},
}
# Evaluate keyword only; preserve exact vocabulary and list; avoid labels misrepresenting.
period_rows=[]
for label,a,b in periods:
  subset=[x for x in R if a<=x['publication_year']<=b]
  for group, terms in termsets.items():
    count=sum(bool(set(terms_by_id[x['id']]) & terms) for x in subset)
    period_rows.append(dict(period=label,tema=group,n_artigos=len(subset),com_termo=count,percent=round(100*count/len(subset),1)))

def references(v):return set(v.get('referenced_works') or [])
refs={v['id']:references(v) for v in R}
refcount=Counter(t for rr in refs.values() for t in rr)
BR=nx.Graph(); BR.add_nodes_from([v['id'] for v in R if refs[v['id']]])
# exact bibliographic coupling shared works (raw overlap); each reference generates co-reference pairs efficiently
ref_docs=defaultdict(list)
for k,rl in refs.items():
 for r in rl:ref_docs[r].append(k)
edgecount=Counter()
for _,docs in sorted(ref_docs.items()):
 for a,b in combinations(sorted(docs),2):edgecount[(a,b)]+=1
for (a,b),w in edgecount.items():
 if w>=2: BR.add_edge(a,b,weight=w)
BM=metrics(BR) if BR.number_of_edges()>0 else {}
# Weighted coupling fraction by nodes and cite coverage.
cross_articles=[(a,b,w) for (a,b),w in edgecount.items() if w>=2]

# country co-authorship collaboration from countries of affiliations; avoid equating author-nationality.
countries={v['id']:sorted({c for auth in v.get('authorships') or [] for c in (auth.get('countries') or []) if c}) for v in R}
C=nx.Graph(); country_freq=Counter(); collaborative=0
for lst in countries.values():
  country_freq.update(lst)
  if len(lst)>=2:collaborative+=1
  for a,b in combinations(lst,2):
    if C.has_edge(a,b):C[a][b]['weight']+=1
    else:C.add_edge(a,b,weight=1)

# Detailed check eligibility set did not accidentally include non-journals; exact raw metadata source.
journal_n=sum((x.get('primary_location') or {}).get('source',{}).get('type')=='journal' if (x.get('primary_location') or {}).get('source') else False for x in R)

# Potential duplicates in the 208 (title normalized) only list, no arbitrary deletion
norms=defaultdict(list)
for v in R:
 normalized=re.sub(r'[^a-z0-9]+',' ',(v['display_name'] or '').lower()).strip()
 norms[normalized].append(v)
exact_dupes={k: vv for k,vv in norms.items() if len(vv)>1}

# Important reference titles where referenced works themselves present in 3,468 retrieved IDs
ref_titles=[]
for id,count in refcount.most_common(20):
   meta=byid.get(id)
   ref_titles.append(dict(id=id, count=count, title=meta['display_name'] if meta else '(não identificado no corpus recuperado)'))

# Publication years and header figures
annual=D.groupby('ano').size().reindex(range(2000,2026),fill_value=0)

plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans','figure.dpi':135})
# 1 publication bars
fig,ax=plt.subplots(figsize=(9.2,3.35))
ax.bar(annual.index,annual.values)
ax.set_title('Núcleo provisório · publicações por ano (2000–2025)')
ax.set_ylabel('Artigos na amostra');ax.set_xticks(range(2000,2026,3));ax.set_ylim(0,max(annual.values)*1.22)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout();fig.savefig(OUT/'fig1_producao_anual.png',bbox_inches='tight',dpi=180);plt.close(fig)

# 2 thematic weighted keyword co-occurrence network, force-directed, limited to 56 labels
fig,ax=plt.subplots(figsize=(11,7.2))
pos=nx.spring_layout(G,seed=23,weight='weight',iterations=160,k=.35)
palette=plt.get_cmap('tab10');group_num={t:i for i,C0 in enumerate(cs) for t in C0}
colors=[palette(group_num[t]%10) for t in G.nodes]
width=[0.2+2.5*math.sqrt(G[u][v]['weight']/max(1,max(strength.values()))) for u,v in G.edges]
nx.draw_networkx_edges(G,pos,ax=ax,alpha=.17,width=width)
nx.draw_networkx_nodes(G,pos,ax=ax,node_size=[27+13*frequency[x] for x in G.nodes],node_color=colors,alpha=.86,linewidths=.5,edgecolors='white')
for name in [t for t,_ in frequency.most_common(23) if t in G.nodes]:
  x,y=pos[name]
  ax.annotate(name,(x,y),fontsize=7 if len(name)>25 else 8,xytext=(2,1),textcoords='offset points')
ax.set_title('Coocorrência de palavras-chave · núcleo provisório (ocorrência ≥ 5)',fontsize=13)
ax.axis('off');fig.tight_layout();fig.savefig(OUT/'fig2_rede_keywords.png',bbox_inches='tight',dpi=200);plt.close(fig)

# 3 term shares by period as table chart to avoid extrapolations
P=pd.DataFrame(period_rows)
fig,ax=plt.subplots(figsize=(10,4.5))
labels=list(termsets.keys()); xs=list(range(len(labels)))
for pi,(lab,_,_) in enumerate(periods):
 sub=P[P.period==lab].set_index('tema').reindex(labels)
 ax.bar([x+(pi-1)*.24 for x in xs],sub['percent'],width=.23,label=lab)
ax.set_xticks(xs,labels,rotation=25,ha='right');ax.set_ylabel('% de artigos com a palavra-chave');ax.set_title('Participação temática nos três períodos (keywords OpenAlex)')
ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False,ncol=3,loc='upper right');fig.tight_layout()
fig.savefig(OUT/'fig3_temas_por_periodo.png',bbox_inches='tight',dpi=175);plt.close(fig)

# 4 coupling bibliographic network, only connected largest 80? Show top connected nodes and all edges >=3 for clarity
B3=nx.Graph(); B3.add_edges_from((u,v,d) for u,v,d in BR.edges(data=True) if d['weight']>=3)
B3.remove_nodes_from(list(nx.isolates(B3)))
if B3.number_of_nodes():
  largest=max(nx.connected_components(B3),key=len)
  H=B3.subgraph(largest).copy()
  communities=detect(H)
  cmap={t:i for i,c in enumerate(communities) for t in c}
  fig,ax=plt.subplots(figsize=(10,6))
  pos=nx.spring_layout(H,seed=42,weight='weight',iterations=150)
  node_ids=list(H.nodes)
  nx.draw_networkx_edges(H,pos,ax=ax,width=.45,alpha=.16)
  nx.draw_networkx_nodes(H,pos,ax=ax,node_color=[palette(cmap[k]%10) for k in node_ids],node_size=[22+22*math.log1p(byid[k]['cited_by_count']) for k in node_ids],alpha=.85)
  topdocs=sorted(node_ids,key=lambda k:byid[k]['cited_by_count'],reverse=True)[:9]
  for a in topdocs:
    label=byid[a]['display_name'];label=label[:36]+'…' if len(label)>39 else label
    ax.annotate(label,pos[a],xytext=(3,2),textcoords='offset points',fontsize=6.5)
  ax.set_title('Acoplamento bibliográfico · ≥ 3 referências em comum (maior componente)')
  ax.axis('off');fig.tight_layout();fig.savefig(OUT/'fig4_rede_acoplamento.png',bbox_inches='tight',dpi=180);plt.close(fig)

# Save machine readable results (CSV is output-data, no spreadsheet workbook edits)
with open(OUT/'indicadores.json','w',encoding='utf8') as f:
 json.dump({
  'universo':len(RAW),'nucleo':len(R),'periodos':[{'periodo':p,'n':len(D[(D.ano>=a)&(D.ano<=b)])} for p,a,b in periods],
  'keywords':{key:{'n':val['n'],'arestas':val['edges'],'forca_total':val['sum_weights'],'componentes':val['components'],'clusters':val['clusters'],'modularidade':round(val['modularity'],4),'frac_forca_entre_clusters':round(val['cross_weight_share'],4)} for key,val in [('min3',M3),('min5',M),('min8',M8),('min5_sem_ancora',M_no)]},
  'acoplamento':{'artigos_com_referencias':len(BR),'links_2mais':BR.number_of_edges(),'pares_1mais':len(edgecount),'maior_componente_2mais':len(max(nx.connected_components(BR),key=len)) if len(BR) else 0,'modularidade':round(BM['modularity'],4) if BM else None,'comunidades':BM.get('clusters')},
  'paises':{'cobertura':sum(bool(x) for x in countries.values()),'artigos_multinacionais':collaborative,'arestas_paises':C.number_of_edges()},
  'duplicacoes_titulos_exatas':{k:[v['id'] for v in vals] for k,vals in exact_dupes.items()},
  'nucleos_sem_resumo':int(D.resumo.isna().sum()),'documentos_sem_refs':int((D.n_referencias==0).sum()),'journal_n':journal_n,
 },f,indent=2,ensure_ascii=False)
for filename,rows in [('temas_periodos.csv',period_rows),('clusters_keyword.csv',cluster_rows),('referencias_centrais.csv',ref_titles),('ranking_termos.csv',[{'termo':s,'ocorrencias':freq,'forca_total':strength.get(s),'grau':G.degree(s) if s in G else None,'betweenness':round(central[s],5) if s in G else None} for s,freq in frequency.most_common(100)])]:
 with open(OUT/filename,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter=';');w.writeheader();w.writerows(rows)
print('KEY NETWORK',[(k,{q:round(v[q],3) if isinstance(v[q],float) else v[q] for q in ['n','edges','sum_weights','clusters','modularity','cross_weight_share']}) for k,v in [('min3',M3),('min5',M),('min8',M8),('no anchor',M_no)]])
print('clusters',cluster_rows)
print('coupling',len(BR),BR.number_of_edges(),len(edgecount),'components',nx.number_connected_components(BR),'max component',len(max(nx.connected_components(BR),key=len)))
print('coauthor affil countries',sum(bool(x) for x in countries.values()),collaborative,C.number_of_edges(),country_freq.most_common(12))
print('periods',pd.DataFrame(period_rows).to_string(index=False))
print('TOP references',ref_titles[:12])
print('exact duplicate titles',len(exact_dupes),sum(len(v) for v in exact_dupes.values()))
print('outputs in',OUT)
