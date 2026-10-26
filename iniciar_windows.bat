@echo off
chcp 65001 >nul
title Hydra
if not exist .venv\Scripts\python.exe (echo Execute instalar_windows.bat primeiro.& pause & exit /b 1)
start "" http://127.0.0.1:5000
.venv\Scripts\python.exe app.py
pause
