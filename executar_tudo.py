#!/usr/bin/env python3
"""Reexecuta todas as análises offline a partir dos dados originais versionados."""
from pathlib import Path
import subprocess,sys,time,os
HERE=Path(__file__).resolve().parent
FILES=['01_validar_fontes.py','02_triagem.py','03_redes_e_figuras.py','04_acoplamento_normalizado.py','05_rede_vosviewer_original.py','06_testes_resultados.py','07_rastrear_resultados.py','08_gerar_relatorio.py']
for f in FILES:
 print(f'\n===== EXECUTANDO {f} =====',flush=True)
 start=time.perf_counter()
 subprocess.run([sys.executable,str(HERE/'scripts'/f)],cwd=HERE,check=True,env={**os.environ,'PYTHONHASHSEED':'0','MPLBACKEND':'Agg'})
 print(f'===== OK {f} ({time.perf_counter()-start:.1f} s) =====',flush=True)
print('\nCONCLUÍDO. Abra resultados/analises, resultados/rastreabilidade e resultados/resumo_reproducibilidade.json.')
