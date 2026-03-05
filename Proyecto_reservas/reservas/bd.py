# conexion a sqlite
import sqlite3
from sqlite3 import Error
from pathlib import Path

db_path = Path(__file__).parent / "data" / "reservas.db"

def get_db_connection():
    db_path.parent.mkdir (parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3. Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                celular TEXT NOT NULL,
                fecha_reserva TEXT NOT NULL,
                personas INTEGER NOT NULL
            )
        """)
        conn.commit()