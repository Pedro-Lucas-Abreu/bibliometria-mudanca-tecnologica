@echo off
cd /d "%~dp0"
python executar_tudo.py
if errorlevel 1 (
 echo.
 echo ERRO. Veja as linhas acima e confira a instalacao de dependencias.
)
pause
