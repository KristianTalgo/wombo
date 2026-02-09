import os
import time
import pymysql
from flask import Flask

app = Flask(__name__)

def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "KristianTalgo"),
        password=os.getenv("DB_PASSWORD", "159355"),
        database=os.getenv("DB_NAME", "wombo"),
        autocommit=True,
    )

def init_db():
    # Sikkerhet: prøv noen ganger hvis DB akkurat startet
    for _ in range(20):
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS visits (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            conn.close()
            return
        except Exception:
            time.sleep(1)

@app.route("/")
def home():
    init_db()
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO visits VALUES (NULL, DEFAULT);")
        cur.execute("SELECT COUNT(*) FROM visits;")
        (count,) = cur.fetchone()
    conn.close()
    return f"Hei! Flask + MariaDB funker 🚀 Antall besøk: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
