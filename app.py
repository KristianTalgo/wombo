import os
import pymysql
from flask import Flask

app = Flask(__name__)


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
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Reneste måte å bruke defaults på i MariaDB/MySQL
            cur.execute("INSERT INTO visits () VALUES ();")

            cur.execute("SELECT COUNT(*) FROM visits;")
            row = cur.fetchone()
            count = int(row[0]) if row else 0

        return f"Hei! Flask + MariaDB funker 🚀 Antall besøk: {count}"
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
