@echo off
chcp 65001 >nul
title Hydra - Inicializador
if not exist .venv\Scripts\python.exe (
  echo Ambiente nao encontrado. Execute instalar_windows.bat primeiro.
  pause
  exit /b 1
)
start "" http://127.0.0.1:5000
.venv\Scripts\python.exe app.py
pause
