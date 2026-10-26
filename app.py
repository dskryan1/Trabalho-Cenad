import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Catálogo demonstrativo. Substitua por produtos reais e preços confirmados.
GAMES = [
    {"name": "Cyberpunk 2077", "category": "PC", "price": "R$ 89,90", "tag": "RPG", "desc": "Explore Night City em um RPG de mundo aberto."},
    {"name": "Hades", "category": "PC", "price": "R$ 24,90", "tag": "Indie", "desc": "Ação rápida e mitologia em uma aventura roguelike."},
    {"name": "Stardew Valley", "category": "PC", "price": "R$ 19,99", "tag": "Relax", "desc": "Construa sua fazenda e viva no seu ritmo."},
    {"name": "Elden Ring", "category": "PC", "price": "R$ 149,90", "tag": "Soulslike", "desc": "Uma aventura desafiadora em um vasto mundo."},
    {"name": "Gift Card PC", "category": "Gift cards", "price": "Consulte", "tag": "Digital", "desc": "Consulte disponibilidade e região antes de comprar."},
    {"name": "Setup de mods", "category": "Serviços", "price": "Sob consulta", "tag": "Mods", "desc": "Ajuda para instalar mods compatíveis e permitidos."},
]

@app.route("/")
def home():
    return render_template("index.html", games=GAMES)

@app.route("/health")
def health():
    return jsonify(status="ok", app="Hydra")

if __name__ == "__main__":
    # Desenvolvimento local: python app.py
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
