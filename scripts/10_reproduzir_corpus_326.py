#!/usr/bin/env python3
"""Reproduz o corpus harmonizado e indicadores; base original congelada, sem API.
O artigo permanece um estudo bibliometrico exploratorio, nao revisao sistematica completa.
"""
from collections import Counter,defaultdict
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import csv,json,statistics,random
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"resultados/harmonizado_326"
OUT.mkdir(parents=True,exist_ok=True)
src=ROOT/"dados/originais_openalex/07_openalex_uniao_vosviewer.json"
ids={x.strip() for x in (ROOT/"dados/harmonizado_326/ids_selecionados.txt").read_text().splitlines() if x.strip()}
assert len(ids)==326
original=json.loads(src.read_text(encoding="utf-8"))["results"]
lookup={r["id"].split("/")[-1]:r for r in original}
assert ids<=lookup.keys(),ids-lookup.keys()
R=[deepcopy(lookup[k]) for k in sorted(ids)]

CORRECTIONS={
"W1482449752":("Finnish Economic Papers",2011),
"W1604955196":("Brussels Economic Review",2013),
"W1803522228":("Australian Bulletin of Labour",2011),
"W188256664":("Economic Review, Federal Reserve Bank of Kansas City",2013),
"W2109270856":("Rivista di Economia e Statistica del Territorio",2006),
"W2123416811":("The Review of Economics and Statistics",2010),
"W2529100062":("Communications & Strategies",2015),
"W2535200922":("Estudios Sociales",2016),
"W2949167907":("Polis",2019),
"W2980001092":("Australasian Journal of Regional Studies",2019),
"W2988830362":("The Japanese Journal of Labour Studies",2011),
"W2346106429":("China Economic Quarterly / 经济学(季刊)",2015),
"W7120002359":("Revista Brasileira de Inovação",2024),
"W7143757227":("Hitotsubashi Journal of Economics",2024),
"W1529037908":("Studies of Applied Economics",2014),
}
for r in R:
 k=r["id"].split("/")[-1]
 if k not in CORRECTIONS:continue
 journal,year=CORRECTIONS[k]
 if r["publication_year"]!=year:
  r["publication_year"]=year
  r["publication_date"]=str(year)+"-01-01"
 s=(r.get("primary_location") or {}).get("source")
 if s:s["display_name"]=journal
 if k=="W7120002359":r["doi"]="https://doi.org/10.20396/rbi.v23i00.8674967"
 if k=="W2123416811":r["display_name"]="Explaining Women's Success: Technological Change and the Skill Content of Women's Work"

(OUT/"corpus_harmonizado_openalex.json").write_text(json.dumps({"meta":{"n":326,"status":"cenario harmonizado conservador; sem leitura integral do corpus"},"results":R},ensure_ascii=False,indent=1),encoding="utf-8")

ALIASES={
"routine-biased technical change":"routine-biased technological change",
"labour market polarization":"labor market polarization",
"occupational polarisation":"occupational polarization",
"job polarisation":"job polarization",
"labour market":"labor market",
"technological unemployment":"technology-induced unemployment"
}
SETS={
"Polarizacao ocupacional":{"job polarization","labor market polarization","occupational polarization","employment polarization"},
"Rotinizacao / RBTC":{"routine-biased technological change","routine tasks","routine occupations"},
"Automacao":{"automation","robotics","industrial robots"},
"Inteligencia artificial":{"artificial intelligence","generative artificial intelligence","generative ai","machine learning","ai technology"},
"Offshoring":{"offshoring"},
"Desigualdade salarial":{"wage inequality","wage polarization","wage distribution"},
}
PERIODS=[("2000–2012",2000,2012),("2013–2018",2013,2018),("2019–2025",2019,2025)]
def savecsv(name,rr):
 if not rr:return
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]),delimiter=";");w.writeheader();w.writerows(rr)
def keywords(x):return sorted({ALIASES.get(k["display_name"].strip().lower(),k["display_name"].strip().lower()) for k in x.get("keywords",[]) if k.get("display_name")})
vocab={r["id"]:keywords(r) for r in R}
freq=Counter(w for ws in vocab.values() for w in ws)
def network(threshold=5,drop_anchor=False):
 sel={t for t,v in freq.items() if v>=threshold and (not drop_anchor or t!="job polarization")}
 g=nx.Graph();g.add_nodes_from(sorted(sel))
 for r in R:
  for a,b in combinations(sorted(set(vocab[r["id"]])&sel),2):
   if g.has_edge(a,b):g[a][b]["weight"]+=1
   else:g.add_edge(a,b,weight=1)
 return g
def communities(g,seed=42):return nx.community.louvain_communities(g,weight="weight",seed=seed,resolution=1.0)
def Q(g,p):return nx.community.modularity(g,p,weight="weight")
g=network();p0=communities(g)
result={"cenario":"corpus_harmonizado_326","artigos":326,"rede_keywords":{
"nos":g.number_of_nodes(),"arestas":g.number_of_edges(),"peso_total":sum(d["weight"] for _,_,d in g.edges(data=True)),
"comunidades":len(p0),"modularidade":round(Q(g,p0),5),"job_polarization":freq["job polarization"]},"sensibilidade":{}}
for lim,drop,key in [(3,False,"min3"),(5,False,"min5"),(8,False,"min8"),(5,True,"min5_sem_job_polarization")]:
 h=network(lim,drop);pp=communities(h)
 result["sensibilidade"][key]={"nos":h.number_of_nodes(),"arestas":h.number_of_edges(),"comunidades":len(pp),"Q":round(Q(h,pp),5)}
tempos=[]
for period,a,b in PERIODS:
 rr=[x for x in R if a<=x.get("publication_year",0)<=b]
 for topic,words in SETS.items():
  n=sum(bool(words&set(vocab[x["id"]])) for x in rr)
  tempos.append({"cenario":"corpus_harmonizado_326","periodo":period,"tema":topic,
    "artigos_periodo":len(rr),"artigos_com_termo":n,"percentual":round(n/len(rr)*100,3) if rr else 0})
result["periodos"]=[{"periodo":p,"n":sum(a<=x["publication_year"]<=b for x in R)} for p,a,b in PERIODS]
result["termos_periodos"]=tempos
savecsv("temas_por_periodo_326.csv",tempos)
refs={x["id"]:set(x.get("referenced_works") or []) for x in R}
have=[x for x in R if refs[x["id"]]]
refdocs=defaultdict(list)
for doc,rlist in refs.items():
 for key in rlist:refdocs[key].append(doc)
edges=Counter()
for docs in refdocs.values():
 for pair in combinations(sorted(docs),2):edges[pair]+=1
nr=len(have);np=nr*(nr-1)//2;ngood=sum(v>=2 for v in edges.values())
result["acoplamento"]={"com_referencias":nr,"sem_referencias":326-nr,
"pares_possiveis":np,"pares_compartilham_2mais":ngood,"porcentagem_pares_2mais":round(100*ngood/np,3)}
rf=Counter(k for rr in refs.values() for k in rr)
savecsv("referencias_mais_utilizadas_326.csv",[{"ref_openalex_id":k,"ocorrencias":v} for k,v in rf.most_common(30)])
P=[communities(g,seed) for seed in range(100)];mods=[Q(g,p) for p in P]
def ari(a,b):
 x={w:i for i,c in enumerate(a) for w in c};y={w:i for i,c in enumerate(b) for w in c}
 ct=Counter((x[k],y[k]) for k in x);ca=Counter(x.values());cb=Counter(y.values())
 c2=lambda n:n*(n-1)//2
 observed=sum(c2(n) for n in ct.values());sa=sum(c2(n) for n in ca.values());sb=sum(c2(n) for n in cb.values())
 expected=sa*sb/c2(len(x));den=(sa+sb)/2-expected
 return (observed-expected)/den if den else 1
result["louvain_100_sementes"]={
"numero_comunidades":dict(Counter(map(len,P))),"ARI_medio_pares":round(statistics.mean(ari(a,b) for a,b in combinations(P,2)),5),
"Q_min":round(min(mods),5),"Q_max":round(max(mods),5)}
savecsv("06_louvain_100_sementes.csv",[{"semente":i,"comunidades":len(p),"modularidade":round(mods[i],6)} for i,p in enumerate(P)])
grp=sorted(p0,key=len,reverse=True);membership={t:i for i,g0 in enumerate(grp) for t in g0}
assigned={};ties=set()
for r in have:
 ct=Counter(membership[k] for k in vocab[r["id"]] if k in membership)
 if not ct:continue
 best=max(ct.values());winners=[k for k,v in ct.items() if v==best]
 if len(winners)>1:ties.add(r["id"])
 assigned[r["id"]]=min(winners)
savecsv("07_artigos_comunidades.csv",[{"openalex_id":r["id"],"titulo":r["display_name"],
"comunidade_predominante":assigned.get(r["id"],"SEM_TERMO_DA_REDE"),
"empate":int(r["id"] in ties),"tem_referencias":int(bool(refs[r["id"]]))} for r in R])
counts=Counter(assigned.values());total=len(assigned)*(len(assigned)-1)//2
pairs_in=sum(n*(n-1)//2 for n in counts.values());pairs_out=total-pairs_in
inside=sum(v>=2 for (a,b),v in edges.items() if a in assigned and b in assigned and assigned[a]==assigned[b])
outside=sum(v>=2 for (a,b),v in edges.items() if a in assigned and b in assigned and assigned[a]!=assigned[b])
obs=inside/pairs_in-outside/pairs_out
rng=random.Random(20261118);keys=list(assigned);labs=[assigned[k] for k in keys]
index={k:i for i,k in enumerate(keys)}
pairs=[(index[a],index[b]) for (a,b),v in edges.items() if v>=2 and a in index and b in index]
extreme=0
for _ in range(999):
 rng.shuffle(labs);cnt=Counter(labs)
 pi=sum(v*(v-1)//2 for v in cnt.values());po=total-pi
 ki=sum(labs[a]==labs[b] for a,b in pairs)
 if abs(ki/pi-(len(pairs)-ki)/po)>=abs(obs):extreme+=1
result["acoplamento_interno_externo"]={
"artigos_com_grupo_e_referencias":len(assigned),"artigos_com_empate":len(ties),
"pares_dentro":pairs_in,"pares_entre":pairs_out,"pares_2mais_dentro":inside,"pares_2mais_entre":outside,
"frac_dentro":round(inside/pairs_in,5),"frac_entre":round(outside/pairs_out,5),
"diferenca_pontos_percentuais":round(obs*100,3),"p_permutacao_bicaudal":(extreme+1)/1000}
(OUT/"resumo_indicadores_recalculados_326.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

# Figuras derivadas exclusivamente das mesmas observacoes e indicadores.
pos=nx.spring_layout(g,seed=23,weight="weight",iterations=200,k=.43)
fig,ax=plt.subplots(figsize=(11,7.3))
nx.draw_networkx_edges(g,pos,edgelist=[(a,b) for a,b,d in g.edges(data=True) if d["weight"]>=3],ax=ax,alpha=.11,width=.6)
cmap=plt.get_cmap("tab10")
nx.draw_networkx_nodes(g,pos,ax=ax,node_color=[cmap(membership[k]%10) for k in g.nodes],node_size=[20+10*freq[k] for k in g.nodes],alpha=.86,linewidths=.45,edgecolors="white")
for key,_ in freq.most_common(9):
 if key in g:ax.annotate(key,pos[key],fontsize=8,xytext=(5,5),textcoords="offset points",bbox={"facecolor":"white","edgecolor":"none","alpha":.75})
ax.set_title("Coocorrencia de palavras-chave · 326 obras");ax.axis("off");fig.tight_layout()
fig.savefig(OUT/"fig1_rede_keywords_326.png",dpi=190,bbox_inches="tight");plt.close(fig)
fig,ax=plt.subplots(figsize=(10,4.7));names=list(SETS)
for j,(period,_,__) in enumerate(PERIODS):
 values={x["tema"]:x["percentual"] for x in tempos if x["periodo"]==period}
 ax.bar([i+(j-1)*.25 for i in range(len(names))],[values.get(k,0) for k in names],width=.24,label=period)
ax.set_xticks(range(len(names)),[k.replace(" ","\n",1) for k in names]);ax.set_ylabel("% dos artigos no periodo");ax.legend(frameon=False,ncol=3)
ax.spines[["top","right"]].set_visible(False);fig.tight_layout()
fig.savefig(OUT/"fig2_temas_periodos_326.png",dpi=190,bbox_inches="tight");plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4));c=Counter(map(len,P))
ax.bar([str(x) for x in sorted(c)],[c[x] for x in sorted(c)]);ax.set_xlabel("Numero de comunidades");ax.set_ylabel("Execucoes (100 sementes)")
ax.spines[["top","right"]].set_visible(False);fig.tight_layout()
fig.savefig(OUT/"fig3_louvain_100_326.png",dpi=180,bbox_inches="tight");plt.close(fig)
fig,ax=plt.subplots(figsize=(6,4))
ax.bar(["Dentro dos grupos","Entre grupos"],[100*inside/pairs_in,100*outside/pairs_out]);ax.set_ylabel("% de pares com 2+ referencias comuns")
ax.spines[["top","right"]].set_visible(False);fig.tight_layout()
fig.savefig(OUT/"fig4_acoplamento_dentro_entre_326.png",dpi=180,bbox_inches="tight");plt.close(fig)
assert (len(R),g.number_of_nodes(),g.number_of_edges(),nr)==(326,91,1269,269)
assert abs(result["rede_keywords"]["modularidade"]-0.11415)<1e-4
print("Verificado: 326 obras, 91 termos, 1269 arestas, Q 0.11415")
