#!/usr/bin/env python3
"""Conferência dos arquivos congelados, sem consultar a Internet.
Requer somente Python 3.10+ (biblioteca padrão)."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, datetime
R=Path(__file__).resolve().parents[1]
IN=R/'dados/originais_openalex'; OUT=R/'resultados/auditoria'; OUT.mkdir(parents=True,exist_ok=True)
def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
manifest=json.loads((R/'dados/manifest_sha256.json').read_text(encoding='utf8'))
checks=[]
for rel,previous in manifest.items():
 p=R/rel
 if not p.exists():raise FileNotFoundError(f'Faltou o arquivo original {p}')
 now=hashlib.sha256(p.read_bytes()).hexdigest()
 checks.append({'arquivo':rel,'sha256':now,'confere_manifesto':now==previous,'bytes':p.stat().st_size})
 if now!=previous:raise RuntimeError(f'ATENÇÃO, dados originais alterados: {rel}')
audit=readcsv(IN/'02_auditoria_buscas.csv')
base=readcsv(IN/'01_base_unificada.csv')
with (IN/'07_openalex_uniao_vosviewer.json').open(encoding='utf8') as f:meta=json.load(f)
raw=meta['results'];ids=[x['id'] for x in raw];csv_ids=[x['openalex_id'] for x in base]
assert len(raw)==len(base)==3468, f'Contagem divergente: {len(raw)}, {len(base)}'
assert len(set(ids))==len(set(csv_ids))==3468
assert set(ids)==set(csv_ids), 'Inconsistência entre CSV e JSON'
total=int(sum(int(x['contagem_api_atual']) for x in audit))
assert total==4975, f'Soma das seis consultas divergente: {total}'
assert all(x['contagem_api_atual']==x['IDs_baixados_unicos_na_consulta'] for x in audit)
assert all(x['contagem_api_atual']==x['contagem_site_anotada'] for x in audit)
with (OUT/'hashes_verificados.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['arquivo','sha256','confere_manifesto','bytes'],delimiter=';');w.writeheader();w.writerows(checks)
result={
 'fonte':'arquivos locais congelados de coleta OpenAlex; não consulta API ao executar',
 'data_processamento_local':datetime.datetime.now().isoformat(timespec='seconds'),
 'consultas':[{k:x[k] for k in ['busca','expressao','contagem_api_atual']} for x in audit],
 'total_aparicoes':total,'registros_unicos':len(base),'aparicoes_excedentes':total-len(base),
 'sem_referencias':sum(not v.get('referenced_works') for v in raw),
 'sem_resumo_indexado':sum(not v.get('abstract_inverted_index') for v in raw),
 'arquivos_originais_hash_ok':len(checks)
}
(OUT/'conferencia_coleta.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('OK — originais intactos:',len(checks),'| aparições nas buscas:',total,'| obras únicas:',len(base))
