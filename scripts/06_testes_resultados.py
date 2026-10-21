#!/usr/bin/env python3
"""Testes de consistência dos resultados recriados — falha se contagens divergem."""
from pathlib import Path
import csv,json,collections
R=Path(__file__).resolve().parents[1];IN=R/'resultados';O=IN/'analises';T=IN/'triagem'
def read(name):
 with name.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
results=read(T/'01_decisoes_3468.csv');c=collections.Counter(x['categoria_triada'] for x in results)
assert len(results)==3468 and dict(c)=={'nucleo_provisorio':208,'revisar':845,'nao_selecionado':2415},dict(c)
core=read(T/'02_nucleo_provisorio.csv'); assert len(core)==208
j=json.loads((O/'indicadores.json').read_text(encoding='utf8'))
assert j['universo']==j['nucleo']==208
assert j['keywords']['min5']['n']==56 and j['keywords']['min5']['arestas']==545
assert j['acoplamento']['artigos_com_referencias']==162
assert j['paises']['cobertura']==165
p=read(O/'temas_periodos.csv'); auto={v['period']:(int(v['n_artigos']),int(v['com_termo'])) for v in p if v['tema']=='Automação'}
assert auto=={'2000–2012':(28,0),'2013–2018':(71,6),'2019–2025':(109,14)},auto
v=json.loads((IN/'vosviewer_exploratorio/indicadores_vosviewer.json').read_text(encoding='utf8'))
assert v['nos']==150 and v['arestas']==3524 and v['comunidades_vosviewer']==5
checks={ 'base_unificada':3468,'nucleo_provisorio':208,'revisao_pendente':845,'nao_selecionados':2415,'keywords_nos_min5':56,'keywords_arestas_min5':545,'documentos_com_referencias':162,'documentos_com_pais':165,'vosviewer_nos':150,'vosviewer_arestas':3524,'resultados_checados':True}
(IN/'resumo_reproducibilidade.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('TODOS OS TESTES PASSARAM. Resumo salvo em resultados/resumo_reproducibilidade.json')
