from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "1234"  # Substitua por uma chave


# ==========================================
# CONEXÃO COM O BANCO
# ==========================================
def get_db_connection():
    conn = sqlite3.connect("clientes.db")
    return conn


# ==========================================
# CRIA A TABELA SE ELA NÃO EXISTIR
# ==========================================
def criar_tabela():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================
@app.route("/")
def interface():
    return render_template("home/interfase.html")

@app.route("/principal")
def principal():
    return render_template("./home/principal.html")



# ==========================================
# LOGIN
# ==========================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )

        usuario = cursor.fetchone()

        conn.close()

        if usuario:
            return redirect(url_for("principal"))
            

        flash("E-mail ou senha incorretos.")
        return redirect(url_for("login"))

    return render_template("login.html")


# ==========================================
# CADASTRO
# ==========================================
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios(nome, email, senha)
                VALUES (?, ?, ?)
            """, (nome, email, senha))

            conn.commit()
            flash("Cadastro realizado com sucesso!")

        except sqlite3.IntegrityError:
            flash("Esse e-mail já está cadastrado.")

        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("registrar.html")


# ==========================================
# EXECUTA O SERVIDOR
# ==========================================
if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)