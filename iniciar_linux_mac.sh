#!/usr/bin/env bash
set -e
source .venv/bin/activate
( sleep 2; python -c "import webbrowser; webbrowser.open('http://127.0.0.1:5000')" ) &
python app.py
