#!/usr/bin/env python3
"""Audita e redesenha o mapa exploratório exportado pelo VOSviewer.
Essa rede tem ORIGEM DIFERENTE da rede feita sobre o núcleo de 208 artigos.
Usa os x/y e clusters exportados pelo VOSviewer, NÃO recalcula seu algoritmo.
"""
from pathlib import Path
from collections import Counter
import csv,json,math
import networkx as nx
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'dados/originais_vosviewer';OUT=ROOT/'resultados/vosviewer_exploratorio';OUT.mkdir(parents=True,exist_ok=True)
with (SRC/'polarizacao_mapa_01.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
with (SRC/'polarizacao_rede_01.csv').open(encoding='utf-8-sig',newline='') as f: edges=list(csv.reader(f))
ids={r['id']:r for r in rows}
g=nx.Graph()
for r in rows:g.add_node(r['id'],**{'nome':r['label'],'cluster':r['cluster'],'ocorrencias':int(r['weight<Occurrences>'])})
for a,b,w in edges:
 if a not in ids or b not in ids:raise ValueError(f'ID ausente do mapa: {a} {b}')
 g.add_edge(a,b,weight=int(w))
assert len(rows)==150 and g.number_of_edges()==3524, 'O mapa original mudou'
cluster_ids=sorted(set(r['cluster'] for r in rows),key=int)
# Duas verificações independentes contra as colunas exportadas
for node,r in ids.items():
 assert g.degree(node)==int(r['weight<Links>']), (node,'grau')
 assert g.degree(node,weight='weight')==int(r['weight<Total link strength>']), (node,'força')
communities=[set(r['id'] for r in rows if r['cluster']==k) for k in cluster_ids]
q=nx.community.modularity(g,communities,weight='weight')
summary={'fonte':'exportação do VOSviewer anterior à união/triagem dos 3468 trabalhos', 'nos':len(rows),'arestas':g.number_of_edges(),'comunidades_vosviewer':len(communities),'forca_somada_pesos':sum(d['weight'] for _,_,d in g.edges(data=True)),'modularidade_calculada_dos_clusters_exportados':round(q,6),'clusters_tamanho':{str(k):len(x) for k,x in zip(cluster_ids,communities)}}
(OUT/'indicadores_vosviewer.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
colors=plt.get_cmap('tab10')
coord={r['id']:(float(r['x']),float(r['y'])) for r in rows}
fig,ax=plt.subplots(figsize=(12,8)); nx.draw_networkx_edges(g,coord,ax=ax,width=.35,alpha=.09)
for i,k in enumerate(cluster_ids):
 selected=[r['id'] for r in rows if r['cluster']==k]
 ax.scatter([coord[n][0] for n in selected],[coord[n][1] for n in selected],s=[13+3*math.sqrt(int(ids[n]['weight<Occurrences>'])) for n in selected],color=colors(i),label=f'Cluster {k} ({len(selected)})',alpha=.8)
for item in sorted(rows,key=lambda x:int(x['weight<Occurrences>']),reverse=True)[:20]:
 ax.annotate(item['label'],coord[item['id']],fontsize=7,xytext=(2,2),textcoords='offset points')
ax.set_title('VOSviewer exploratório · posições e comunidades exportadas (corpus inicial)')
ax.legend(frameon=False,loc='upper left',fontsize=8);ax.axis('off');fig.tight_layout()
fig.savefig(OUT/'mapa_vosviewer_exportado.png',dpi=180,bbox_inches='tight');plt.close(fig)
print('VOSviewer original, verificado:',summary)
