import os
import pymysql
from flask import Flask, request, redirect, session
from markupsafe import escape

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

def get_conn():
    # Gjør variablene eksplisitte (Pylance liker dette)
    host: str = os.getenv("DB_HOST", "db")
    port: int = int(os.getenv("DB_PORT", "3306"))
    user: str = os.getenv("DB_USER", "wombo")
    password: str = os.getenv("DB_PASSWORD", "wombopass")
    database: str = os.getenv("DB_NAME", "wombo")

    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        autocommit=True,
    )


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login") 
    else:
        return redirect("/notes")
    
@app.get("/notes")
def list_notes():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, content, created_at FROM notes WHERE user_id=%s ORDER BY id DESC;", (session["user_id"],))
            rows = cur.fetchall()
        items = "".join([
            f"<li>#{r[0]}: {escape(r[1])} <small>({r[2]})</small></li>"
            for r in rows
        ])
        return f"""
        <h1>Notater</h1>
        <form method="POST" action="/notes">
          <input name="content" placeholder="Skriv notat..." />
          <button type="submit">Legg til</button>
        </form>
        <ul>{items}</ul>
        <a href="/login">Tilbake</a>
        """
    finally:
        conn.close()

@app.post("/notes")
def create_note():
    if "user_id" not in session:
        return redirect("/login")

    content = (request.form.get("content") or "").strip()
    if not content:
        return redirect("/notes")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s);", (session["user_id"], content))
        return redirect("/notes")
    finally:
        conn.close()


@app.get("/login")
def login_form():
    return """
    <h1>Logg inn</h1>
    <form method="POST" action="/login">
      <input name="email" type="email" placeholder="E-post" required />
      <button type="submit">Logg inn</button>
    </form>
    <a href="/">Tilbake</a>
    """

@app.post("/login")
def login_submit():
    email = (request.form.get("email") or "").strip().lower()
    if not email:
        return redirect("/login")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email=%s LIMIT 1;", (email,))
            row = cur.fetchone()

        if not row:
            # Ikke funnet i DB -> ikke logg inn
            return f"""
            <h1>Ingen tilgang</h1>
            <p>E-posten <b>{escape(email)}</b> finnes ikke i systemet.</p>
            <a href="/login">Prøv igjen</a>
            """

        user_id = int(row[0])
        session["user_id"] = user_id
        return redirect("/notes")
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
