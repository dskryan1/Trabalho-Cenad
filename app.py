import os, sqlite3, secrets
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-secret-key")
DB_PATH = os.environ.get("HYDRA_DB", os.path.join(os.path.dirname(__file__), "hydra.db"))

PRODUCTS = [
 {"id":1,"name":"Red Dead Redemption 2","category":"Jogos","price":89.90,"image":"game-rdr.jpg","tag":"Aventura","desc":"Uma aventura de mundo aberto."},
 {"id":2,"name":"Cyberpunk 2077","category":"Jogos","price":99.90,"image":"game-cyber.jpg","tag":"RPG","desc":"Explore uma metrópole futurista."},
 {"id":3,"name":"Elden Ring","category":"Jogos","price":119.90,"image":"game-elden.jpg","tag":"RPG","desc":"Uma jornada de fantasia desafiadora."},
 {"id":4,"name":"Minecraft","category":"Jogos","price":59.90,"image":"game-minecraft.jpg","tag":"Criatividade","desc":"Construa, explore e crie seu mundo."},
 {"id":5,"name":"Forza Horizon 5","category":"Jogos","price":79.90,"image":"game-forza.jpg","tag":"Corrida","desc":"Corra por paisagens abertas."},
 {"id":6,"name":"Gift Card Steam R$ 50","category":"Gift Cards","price":50.00,"image":"gift-steam.jpg","tag":"DEMO ESCOLAR","desc":"Cartão fictício para demonstração escolar."},
 {"id":7,"name":"Gift Card PlayStation R$ 100","category":"Gift Cards","price":100.00,"image":"gift-playstation.jpg","tag":"DEMO ESCOLAR","desc":"Cartão fictício para demonstração escolar."},
 {"id":8,"name":"Gift Card Xbox R$ 100","category":"Gift Cards","price":100.00,"image":"gift-xbox.jpg","tag":"DEMO ESCOLAR","desc":"Cartão fictício para demonstração escolar."},
 {"id":9,"name":"Gift Card Google Play R$ 50","category":"Gift Cards","price":50.00,"image":"gift-google.jpg","tag":"DEMO ESCOLAR","desc":"Cartão fictício para demonstração escolar."},
 {"id":10,"name":"Configuração de mods","category":"Serviços","price":29.90,"image":"game-minecraft.jpg","tag":"Serviço","desc":"Demonstração de serviço de configuração."},
]
def db():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
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
def current_user():
    uid=session.get("user_id")
    if not uid: return None
    with db() as conn:
        row=conn.execute("SELECT id,name,username,email FROM users WHERE id=?",(uid,)).fetchone()
        return dict(row) if row else None
def login_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        if not current_user():
            flash("Entre na sua conta para continuar.","warning")
            return redirect(url_for("login", next=request.path))
        return fn(*args,**kwargs)
    return wrapper
def cart_items():
    cart=session.get("cart",{})
    result=[]
    for p in PRODUCTS:
        qty=int(cart.get(str(p["id"]),0))
        if qty>0: result.append({**p,"qty":qty,"subtotal":round(p["price"]*qty,2)})
    return result
@app.context_processor
def inject():
    items=cart_items()
    return {"current_user":current_user(),"cart_count":sum(x["qty"] for x in items),"cart_total":sum(x["subtotal"] for x in items)}
@app.route("/")
def home():
    category=request.args.get("categoria","Todos")
    q=request.args.get("q","").strip().lower()
    products=[p for p in PRODUCTS if (category=="Todos" or p["category"]==category) and (not q or q in p["name"].lower() or q in p["desc"].lower())]
    return render_template("index.html",products=products,category=category,q=request.args.get("q",""))
@app.route("/cadastro",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip()
        username=request.form.get("username","").strip()
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        confirm=request.form.get("confirm","")
        if not all([name,username,email,password]):
            flash("Preencha todos os campos.","error")
        elif len(password)<8:
            flash("A senha precisa ter pelo menos 8 caracteres.","error")
        elif password!=confirm:
            flash("As senhas não coincidem.","error")
        else:
            try:
                with db() as conn:
                    cur=conn.execute("INSERT INTO users(name,username,email,password_hash) VALUES(?,?,?,?)",
                      (name,username,email,generate_password_hash(password)))
                    session.clear(); session["user_id"]=cur.lastrowid
                flash("Conta criada com sucesso! Este é um projeto demonstrativo.","success")
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("Esse usuário ou e-mail já está cadastrado.","error")
    return render_template("auth.html",mode="register")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        identifier=request.form.get("identifier","").strip().lower()
        password=request.form.get("password","")
        with db() as conn:
            user=conn.execute("SELECT * FROM users WHERE lower(email)=? OR lower(username)=?",(identifier,identifier)).fetchone()
        if user and check_password_hash(user["password_hash"],password):
            session.clear(); session["user_id"]=user["id"]
            flash("Login realizado com sucesso.","success")
            return redirect(request.args.get("next") or url_for("home"))
        flash("Usuário/e-mail ou senha inválidos.","error")
    return render_template("auth.html",mode="login")
@app.route("/sair")
def logout():
    session.clear(); flash("Você saiu da sua conta.","success"); return redirect(url_for("home"))
@app.route("/adicionar/<int:product_id>",methods=["POST"])
def add_to_cart(product_id):
    if not any(p["id"]==product_id for p in PRODUCTS): abort(404)
    cart=session.get("cart",{})
    key=str(product_id); cart[key]=min(int(cart.get(key,0))+1,20)
    session["cart"]=cart
    flash("Produto adicionado ao carrinho demonstrativo.","success")
    return redirect(request.referrer or url_for("home"))
@app.route("/carrinho")
def cart():
    return render_template("cart.html",items=cart_items())
@app.route("/quantidade/<int:product_id>",methods=["POST"])
def quantity(product_id):
    cart=session.get("cart",{}); key=str(product_id)
    qty=int(request.form.get("qty",1))
    if qty<=0: cart.pop(key,None)
    else: cart[key]=min(qty,20)
    session["cart"]=cart
    return redirect(url_for("cart"))
@app.route("/finalizar",methods=["GET","POST"])
@login_required
def checkout():
    items=cart_items()
    if not items:
        flash("Seu carrinho está vazio.","warning"); return redirect(url_for("home"))
    if request.method=="POST":
        # Educational demo only: no payment is collected and no real gift card/game is delivered.
        summary="; ".join(f'{x["name"]} x{x["qty"]}' for x in items)
        with db() as conn:
            conn.execute("INSERT INTO orders(user_id,items,total,status) VALUES(?,?,?,'DEMO - NÃO PAGO')",
                         (session["user_id"],summary,round(sum(x["subtotal"] for x in items),2)))
        session["cart"]={}
        return render_template("success.html",items=items,total=sum(x["subtotal"] for x in items))
    return render_template("checkout.html",items=items,total=sum(x["subtotal"] for x in items))
@app.route("/minha-conta")
@login_required
def account():
    user=current_user()
    with db() as conn:
        orders=conn.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",(user["id"],)).fetchall()
    return render_template("account.html",user=user,orders=orders)
@app.route("/health")
def health(): return {"status":"ok","app":"Hydra"}
with app.app_context(): init_db()
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=True)
