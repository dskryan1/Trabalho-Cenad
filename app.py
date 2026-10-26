"""HYDRA — loja gamer DEMONSTRATIVA (projeto escolar).
Nenhum pagamento real, nenhuma entrega real. Tudo é simulação."""
import os, re, random, sqlite3
from functools import wraps
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, abort, jsonify)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-secret-key")
DB_PATH = os.environ.get("HYDRA_DB", os.path.join(os.path.dirname(__file__), "hydra.db"))
MAX_QTY = 10

# ------------------------------------------------------------------ catálogo
CATEGORIES = [
    {"slug": "jogos",       "name": "Jogos",                 "menu": "Jogos",        "icon": "🎮",
     "desc": "Jogos para PC em formato digital.",                      "ratio": "poster"},
    {"slug": "gift-cards",  "name": "Gift Cards",            "menu": "Gift Cards",   "icon": "🎁",
     "desc": "Cartões-presente de lojas e plataformas.",               "ratio": "banner"},
    {"slug": "otimizacao",  "name": "Serviços de Otimização", "menu": "Otimização",   "icon": "⚡",
     "desc": "Deixe o PC mais rápido, estável e pronto pra jogar.",    "ratio": "banner"},
    {"slug": "mods",        "name": "Mods",                  "menu": "Mods",         "icon": "🧩",
     "desc": "Pacotes de mods, texturas e shaders.",                   "ratio": "banner"},
    {"slug": "upamento",    "name": "Upamento de Contas",    "menu": "Upamento",     "icon": "📈",
     "desc": "Evolução de nível, rank e recursos da sua conta.",       "ratio": "banner"},
]
CAT_BY_SLUG = {c["slug"]: c for c in CATEGORIES}

_pid = 0
def P(cat, name, price, image, tag, desc):
    global _pid; _pid += 1
    return {"id": _pid, "category": cat, "name": name, "price": price,
            "image": image, "tag": tag, "desc": desc}

PRODUCTS = [
    # Jogos
    P("jogos", "Red Dead Redemption 2", 89.90, "game-rdr.jpg", "Aventura", "Faroeste de mundo aberto cheio de histórias."),
    P("jogos", "Cyberpunk 2077", 99.90, "game-cyber.jpg", "RPG", "Explore uma metrópole futurista."),
    P("jogos", "Elden Ring", 119.90, "game-elden.jpg", "RPG", "Fantasia sombria e desafiadora."),
    P("jogos", "Minecraft", 59.90, "game-minecraft.jpg", "Sandbox", "Construa, explore e crie seu mundo."),
    P("jogos", "Forza Horizon 5", 79.90, "game-forza.jpg", "Corrida", "Corra por paisagens abertas."),
    P("jogos", "God of War", 89.90, "game-gow.jpg", "Ação", "Mitologia, combate e emoção."),
    P("jogos", "EA Sports FC", 149.90, "game-fc.jpg", "Esporte", "Futebol com times e modos online."),
    P("jogos", "Call of Duty", 199.90, "game-cod.jpg", "FPS", "Tiro em primeira pessoa e multiplayer."),
    # Gift cards
    P("gift-cards", "Gift Card Steam R$ 50", 50.00, "gift-steam.jpg", "Demo", "Cartão fictício para demonstração."),
    P("gift-cards", "Gift Card PlayStation R$ 100", 100.00, "gift-playstation.jpg", "Demo", "Cartão fictício para demonstração."),
    P("gift-cards", "Gift Card Xbox R$ 100", 100.00, "gift-xbox.jpg", "Demo", "Cartão fictício para demonstração."),
    P("gift-cards", "Gift Card Google Play R$ 50", 50.00, "gift-google.jpg", "Demo", "Cartão fictício para demonstração."),
    P("gift-cards", "Gift Card Nintendo R$ 100", 100.00, "gift-nintendo.jpg", "Demo", "Cartão fictício para demonstração."),
    P("gift-cards", "Gift Card Roblox R$ 50", 50.00, "gift-roblox.jpg", "Demo", "Cartão fictício para demonstração."),
    # Otimização
    P("otimizacao", "Otimização completa de PC", 49.90, "opt-pc.jpg", "Serviço", "Limpeza, ajustes de sistema e inicialização."),
    P("otimizacao", "Boost de FPS", 39.90, "opt-fps.jpg", "Serviço", "Configurações gráficas para mais quadros."),
    P("otimizacao", "Ajuste de rede e ping", 34.90, "opt-rede.jpg", "Serviço", "Configuração de rede para jogos online."),
    P("otimizacao", "Formatação + instalação de jogos", 89.90, "opt-formatacao.jpg", "Serviço", "Sistema limpo e jogos instalados."),
    P("otimizacao", "Limpeza e revisão de drivers", 29.90, "opt-limpeza.jpg", "Serviço", "Drivers atualizados e arquivos temporários removidos."),
    # Mods
    P("mods", "Pacote de Mods Minecraft", 24.90, "mod-minecraft.jpg", "Mods", "Coleção de mods populares para Minecraft."),
    P("mods", "Texturas HD Realistas", 19.90, "mod-texturas.jpg", "Texturas", "Visual renovado com texturas em alta resolução."),
    P("mods", "Pacote de Mods Skyrim", 29.90, "mod-skyrim.jpg", "Mods", "Gráficos e melhorias de jogabilidade."),
    P("mods", "Shaders Cinematográficos", 22.90, "mod-shaders.jpg", "Shaders", "Iluminação e efeitos de cinema."),
    P("mods", "Instalação de mods assistida", 29.90, "mod-instalacao.jpg", "Serviço", "Instalação e configuração dos seus mods."),
    # Upamento
    P("upamento", "Upamento de nível (1–50)", 59.90, "up-nivel.jpg", "Nível", "Evolução de nível da conta em jogos de RPG."),
    P("upamento", "Evolução de rank", 79.90, "up-rank.jpg", "Rank", "Subida de rank em jogos competitivos."),
    P("upamento", "Farm de recursos e moedas", 34.90, "up-farm.jpg", "Farm", "Coleta de recursos dentro do jogo."),
    P("upamento", "Conclusão de missões", 44.90, "up-missoes.jpg", "Missões", "Missões principais e secundárias concluídas."),
    P("upamento", "Pacote completo de evolução", 129.90, "up-pacote.jpg", "Combo", "Nível, recursos e missões em um só pacote."),
]
PRODUCT_BY_ID = {p["id"]: p for p in PRODUCTS}

COUPONS = {"HYDRA10": 0.10, "ESCOLA20": 0.20}

def brl(v):
    s = f"{v:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")
app.jinja_env.filters["brl"] = brl

# ------------------------------------------------------------------ banco
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE,
          password_hash TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS orders(
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
          items TEXT NOT NULL, total REAL NOT NULL, status TEXT NOT NULL DEFAULT 'DEMO',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(user_id) REFERENCES users(id))""")
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(orders)")}
        if "code" not in cols:       conn.execute("ALTER TABLE orders ADD COLUMN code TEXT")
        if "pay_method" not in cols: conn.execute("ALTER TABLE orders ADD COLUMN pay_method TEXT")

def current_user():
    uid = session.get("user_id")
    if not uid: return None
    with db() as conn:
        row = conn.execute("SELECT id,name,username,email FROM users WHERE id=?", (uid,)).fetchone()
    return dict(row) if row else None

def login_required(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        if not current_user():
            flash("Entre na sua conta para continuar.", "warning")
            return redirect(url_for("login", next=request.path))
        return fn(*a, **kw)
    return wrapper

def safe_next(target):
    if not target: return url_for("home")
    u = urlparse(target)
    return target if (not u.netloc and not u.scheme and target.startswith("/") and not target.startswith("//")) else url_for("home")

# ------------------------------------------------------------------ carrinho
def cart_summary():
    cart = session.get("cart", {})
    items = []
    for pid, qty in cart.items():
        p = PRODUCT_BY_ID.get(int(pid))
        qty = int(qty)
        if p and qty > 0:
            items.append({**p, "qty": qty, "subtotal": round(p["price"] * qty, 2),
                          "cat_name": CAT_BY_SLUG[p["category"]]["name"],
                          "image_url": url_for("static", filename="images/" + p["image"])})
    subtotal = round(sum(i["subtotal"] for i in items), 2)
    code = session.get("coupon")
    rate = COUPONS.get(code, 0) if items else 0
    discount = round(subtotal * rate, 2)
    return {"items": items, "count": sum(i["qty"] for i in items), "subtotal": subtotal,
            "coupon": code if rate else None, "rate": rate, "discount": discount,
            "total": round(subtotal - discount, 2)}

def cart_json():
    s = cart_summary()
    return {**s, "subtotal_fmt": brl(s["subtotal"]), "discount_fmt": brl(s["discount"]),
            "total_fmt": brl(s["total"]),
            "items": [{**i, "price_fmt": brl(i["price"]), "subtotal_fmt": brl(i["subtotal"])} for i in s["items"]]}

@app.context_processor
def inject():
    s = cart_summary()
    return {"current_user": current_user(), "cart_count": s["count"], "cart_total": s["total"],
            "categories": CATEGORIES,
            "cat_counts": {c["slug"]: sum(1 for p in PRODUCTS if p["category"] == c["slug"]) for c in CATEGORIES}}

def wants_json():
    return request.is_json or request.headers.get("X-Requested-With") == "fetch"

# ------------------------------------------------------------------ páginas
HOME_PER_CATEGORY = 4

@app.route("/")
def home():
    q = request.args.get("q", "").strip()
    ql = q.lower()
    sections = []
    for c in CATEGORIES:
        items = [p for p in PRODUCTS if p["category"] == c["slug"]
                 and (not ql or ql in p["name"].lower() or ql in p["desc"].lower() or ql in p["tag"].lower())]
        if not items: continue
        sections.append({"cat": c, "total": len(items),
                         "products": items if ql else items[:HOME_PER_CATEGORY]})
    return render_template("index.html", sections=sections, q=q)

@app.route("/categoria/<slug>")
def category(slug):
    c = CAT_BY_SLUG.get(slug) or abort(404)
    sort = request.args.get("ordem", "")
    items = [p for p in PRODUCTS if p["category"] == slug]
    if sort == "menor": items.sort(key=lambda p: p["price"])
    elif sort == "maior": items.sort(key=lambda p: -p["price"])
    elif sort == "nome": items.sort(key=lambda p: p["name"])
    return render_template("categoria.html", cat=c, products=items, sort=sort)

@app.route("/suporte")
def support():
    return render_template("suporte.html")

# ------------------------------------------------------------------ conta
@app.route("/cadastro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not all([name, username, email, password]):
            flash("Preencha todos os campos.", "error")
        elif len(password) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres.", "error")
        elif password != confirm:
            flash("As senhas não coincidem.", "error")
        else:
            try:
                with db() as conn:
                    cur = conn.execute("INSERT INTO users(name,username,email,password_hash) VALUES(?,?,?,?)",
                                       (name, username, email, generate_password_hash(password)))
                    cart, coupon = session.get("cart", {}), session.get("coupon")
                    session.clear(); session["user_id"] = cur.lastrowid
                    session["cart"], session["coupon"] = cart, coupon
                flash("Conta criada com sucesso! Este é um projeto demonstrativo.", "success")
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("Esse usuário ou e-mail já está cadastrado.", "error")
    return render_template("auth.html", mode="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ident = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")
        with db() as conn:
            user = conn.execute("SELECT * FROM users WHERE lower(email)=? OR lower(username)=?", (ident, ident)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            cart, coupon = session.get("cart", {}), session.get("coupon")
            session.clear(); session["user_id"] = user["id"]
            session["cart"], session["coupon"] = cart, coupon
            flash("Login realizado com sucesso.", "success")
            return redirect(safe_next(request.args.get("next")))
        flash("Usuário/e-mail ou senha inválidos.", "error")
    return render_template("auth.html", mode="login")

@app.route("/sair")
def logout():
    session.clear(); flash("Você saiu da sua conta.", "success")
    return redirect(url_for("home"))

@app.route("/minha-conta")
@login_required
def account():
    user = current_user()
    with db() as conn:
        orders = conn.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC", (user["id"],)).fetchall()
    return render_template("account.html", user=user, orders=orders)

# ------------------------------------------------------------------ carrinho (rotas)
@app.route("/adicionar/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    p = PRODUCT_BY_ID.get(product_id) or abort(404)
    cart = session.get("cart", {}); key = str(product_id)
    cart[key] = min(int(cart.get(key, 0)) + 1, MAX_QTY)
    session["cart"] = cart
    if wants_json():
        return jsonify({"ok": True, "message": f"{p['name']} adicionado ao carrinho", "cart": cart_json()})
    flash("Produto adicionado ao carrinho.", "success")
    return redirect(request.referrer or url_for("home"))

@app.route("/api/carrinho")
def api_cart():
    return jsonify(cart_json())

@app.route("/api/carrinho/<int:product_id>", methods=["POST"])
def api_cart_set(product_id):
    """Define a quantidade (qty<=0 remove). Retorna o carrinho recalculado."""
    if product_id not in PRODUCT_BY_ID: abort(404)
    data = request.get_json(silent=True) or {}
    try: qty = int(data.get("qty", 1))
    except (TypeError, ValueError): qty = 1
    cart = session.get("cart", {}); key = str(product_id)
    if qty <= 0: cart.pop(key, None)
    else: cart[key] = min(qty, MAX_QTY)
    session["cart"] = cart
    return jsonify(cart_json())

@app.route("/api/cupom", methods=["POST"])
def api_coupon():
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip().upper()
    if not code:
        session.pop("coupon", None)
        return jsonify({"ok": True, "message": "Cupom removido.", "cart": cart_json()})
    if code in COUPONS:
        session["coupon"] = code
        return jsonify({"ok": True, "message": f"Cupom {code} aplicado: {int(COUPONS[code]*100)}% de desconto!", "cart": cart_json()})
    return jsonify({"ok": False, "message": "Cupom inválido. Tente HYDRA10 ou ESCOLA20.", "cart": cart_json()}), 400

@app.route("/carrinho")
def cart():
    return render_template("cart.html", cart=cart_summary())

@app.route("/quantidade/<int:product_id>", methods=["POST"])  # fallback sem JavaScript
def quantity(product_id):
    cart = session.get("cart", {}); key = str(product_id)
    try: qty = int(request.form.get("qty", 1))
    except ValueError: qty = 1
    if qty <= 0: cart.pop(key, None)
    else: cart[key] = min(qty, MAX_QTY)
    session["cart"] = cart
    return redirect(url_for("cart"))

# ------------------------------------------------------------------ checkout FAKE
@app.route("/finalizar", methods=["GET", "POST"])
def checkout():
    s = cart_summary()
    if not s["items"]:
        flash("Seu carrinho está vazio.", "warning"); return redirect(url_for("home"))
    user = current_user()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        method = request.form.get("method", "pix")
        if method not in ("pix", "cartao"): method = "pix"
        if not name or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Informe um nome e um e-mail válidos (podem ser fictícios).", "error")
            return render_template("checkout.html", cart=s, user=user, form=request.form)
        # Simulação: NENHUMA cobrança. Dados de cartão nem chegam ao servidor (campos sem "name").
        code = "HYD-" + "".join(random.choices("0123456789", k=6))
        summary = "; ".join(f'{i["name"]} x{i["qty"]}' for i in s["items"])
        if user:
            with db() as conn:
                conn.execute("INSERT INTO orders(user_id,items,total,status,code,pay_method) VALUES(?,?,?,?,?,?)",
                             (user["id"], summary, s["total"], "DEMO - NÃO PAGO", code, method))
        session["last_order"] = {"code": code, "name": name, "email": email, "method": method,
                                 "items": [{k: i[k] for k in ("name", "qty", "subtotal")} for i in s["items"]],
                                 "subtotal": s["subtotal"], "discount": s["discount"], "total": s["total"],
                                 "coupon": s["coupon"]}
        session["cart"] = {}; session.pop("coupon", None)
        return redirect(url_for("order_success"))
    return render_template("checkout.html", cart=s, user=user, form={})

@app.route("/pedido-concluido")
def order_success():
    order = session.get("last_order")
    if not order: return redirect(url_for("home"))
    return render_template("success.html", o=order)

@app.route("/health")
def health():
    return {"status": "ok", "app": "Hydra"}

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)),
            debug=os.environ.get("FLASK_DEBUG", "1") == "1")
