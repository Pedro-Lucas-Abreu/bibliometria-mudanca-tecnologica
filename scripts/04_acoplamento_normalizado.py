"""Reproduz indicadores da rede de acoplamento normalizada publicada no relatorio.
Requer: networkx, pandas, matplotlib. Usa arquivos locais do pacote.
"""
from pathlib import Path
from collections import defaultdict,Counter
from itertools import combinations
import json,math
import networkx as nx
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
results=json.load(open(ROOT/'resultados/triagem/05_nucleo_provisorio_openalex.json',encoding='utf8'))['results']
R={r['id']:r for r in results}
refs={id:set(r.get('referenced_works') or []) for id,r in R.items()}
refdocs=defaultdict(list)
for id,rr in refs.items():
 for r in rr:refdocs[r].append(id)
shared=Counter()
for _,ids in sorted(refdocs.items()):
 for pair in combinations(sorted(ids),2):shared[pair]+=1
cands=defaultdict(list)
for (a,b),common in shared.items():
 if common>=2:
  sim=common/math.sqrt(len(refs[a])*len(refs[b]))
  cands[a].append((b,sim));cands[b].append((a,sim))
g=nx.Graph();g.add_nodes_from(id for id,rr in refs.items() if rr)
for id,others in sorted(cands.items()):
 for b,sim in sorted(others,key=lambda x:(-x[1], x[0]))[:5]:g.add_edge(id,b,weight=sim)
main=g.subgraph(max(nx.connected_components(g),key=len)).copy()
comm=nx.community.louvain_communities(main,weight='weight',seed=42)
print('Artigos com refs',len(g),'arestas k=5',g.number_of_edges(),'maior componente',len(main),'clusters',len(comm),'Q',round(nx.community.modularity(g,nx.community.louvain_communities(g,weight='weight',seed=42),weight='weight'),3))
positions=nx.spring_layout(main,seed=42,weight='weight',iterations=150,k=.28)
clusters={id:i for i,part in enumerate(comm) for id in part}
fig,ax=plt.subplots(figsize=(10,6.5))
nx.draw_networkx_edges(main,positions,ax=ax,width=.55,alpha=.15)
nx.draw_networkx_nodes(main,positions,ax=ax,nodelist=list(main.nodes),node_color=[clusters[id] for id in main.nodes],cmap='tab10',node_size=[20+10*math.log1p(R[id]['cited_by_count']) for id in main.nodes],alpha=.85)
ax.axis('off');ax.set_title('Acoplamento bibliográfico, similaridade normalizada, k = 5')
fig.tight_layout();dest=ROOT/'resultados/analises/fig5_acoplamento_normalizado_k5.png';fig.savefig(dest,dpi=200)
print('Gráfico salvo em',dest)
