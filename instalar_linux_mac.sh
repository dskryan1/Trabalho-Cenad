#!/usr/bin/env bash
set -e
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Instalação concluída. Execute ./iniciar_linux_mac.sh"
