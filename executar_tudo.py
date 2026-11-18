#!/usr/bin/env python3
"""Executa a reprodução offline do corpus vigente (326) ou do histórico (208)."""
from pathlib import Path
import argparse,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--historico-208",action="store_true",help="Reproduzir os nove scripts do cenário histórico de 208 registros")
args=parser.parse_args()
old=["01_validar_fontes.py","02_triagem.py","03_redes_e_figuras.py","04_acoplamento_normalizado.py","05_rede_vosviewer_original.py","06_testes_resultados.py","07_rastrear_resultados.py","08_gerar_relatorio.py","09_evolucao_keywords.py"]
for name in (old if args.historico_208 else ["10_reproduzir_corpus_326.py"]):
 print("\n===== EXECUTANDO",name,"=====",flush=True)
 t=time.perf_counter()
 subprocess.run([sys.executable,str(ROOT/"scripts"/name)],cwd=ROOT,check=True,env={**os.environ,"PYTHONHASHSEED":"0","MPLBACKEND":"Agg"})
 print("===== OK",name,"(",round(time.perf_counter()-t,1),"s) =====",flush=True)
print("Saídas em", "resultados/analises (histórico)" if args.historico_208 else "resultados/harmonizado_326 (vigente)")
