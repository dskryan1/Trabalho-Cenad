@echo off
chcp 65001 >nul
title Instalador Hydra
where py >nul 2>nul
if errorlevel 1 (echo Instale Python 3.13 e marque Add Python to PATH.& pause & exit /b 1)
py -3.13 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Instalacao concluida. Execute iniciar_windows.bat.
pause
