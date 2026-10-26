@echo off
chcp 65001 >nul
title Instalador Hydra
echo ========================================
echo       INSTALADOR DO SITE HYDRA
echo ========================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale Python 3.13 e marque "Add Python to PATH".
  pause
  exit /b 1
)
py -3.13 -m venv .venv
if errorlevel 1 (
  echo Nao foi possivel criar o ambiente Python 3.13.
  pause
  exit /b 1
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo Falha ao instalar dependencias.
  pause
  exit /b 1
)
echo.
echo Instalacao concluida. Execute iniciar_windows.bat para abrir o site.
pause
