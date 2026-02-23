import os
from pathlib import Path
import pymysql
import time


BASE_DIR = Path(__file__).resolve().parent

# Støtt både norsk og engelsk mappenavn
CANDIDATES = [
    BASE_DIR / "migrations",
    BASE_DIR / "migrasjoner",
    BASE_DIR / "db" / "migrasjoner",
]

MIGRATIONS_DIR = next((p for p in CANDIDATES if p.exists() and p.is_dir()), None)

def wait_for_db(max_tries=30, delay=1):
    for _ in range(max_tries):
        try:
            conn = get_conn()
            conn.close()
            return
        except Exception:
            time.sleep(delay)
    raise RuntimeError("DB ble ikke klar i tide")


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "wombo"),
        password=os.getenv("DB_PASSWORD", "wombopass"),
        database=os.getenv("DB_NAME", "wombo"),
        autocommit=True,
    )


def ensure_migrations_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


def already_applied(conn, filename: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM schema_migrations WHERE filename=%s LIMIT 1;",
            (filename,),
        )
        return cur.fetchone() is not None


def mark_applied(conn, filename: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO schema_migrations (filename) VALUES (%s);",
            (filename,),
        )


def apply_migrations():
    wait_for_db()
    print("BASE_DIR =", BASE_DIR)

    if MIGRATIONS_DIR is None:
        raise RuntimeError(
            "Fant ingen migrasjonsmappe. Lag en av disse:\n"
            "- migrations/\n- migrasjoner/\n- db/migrasjoner/\n"
        )

    print("MIGRATIONS_DIR =", MIGRATIONS_DIR)

    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    print("FOUND SQL FILES =", [p.name for p in files])

    if not files:
        raise RuntimeError(f"Ingen .sql-filer funnet i {MIGRATIONS_DIR}")

    conn = get_conn()
    try:
        ensure_migrations_table(conn)

        for path in files:
            filename = path.name
            if already_applied(conn, filename):
                continue

            sql = path.read_text(encoding="utf-8")

            # kjør statements separert på ;
            statements = [s.strip() for s in sql.split(";") if s.strip()]
            for stmt in statements:
                with conn.cursor() as cur:
                    cur.execute(stmt)

            mark_applied(conn, filename)
            print(f"✅ Applied migration: {filename}")

    finally:
        conn.close()


if __name__ == "__main__":
    apply_migrations()
