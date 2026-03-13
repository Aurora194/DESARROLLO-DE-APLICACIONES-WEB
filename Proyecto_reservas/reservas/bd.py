# conexion a sqlite
import sqlite3
from sqlite3 import Error
from pathlib import Path


db_path = Path(__file__).parent / "data" / "Reservas.db"

def get_db_connection():
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:

        # CLIENTES
        conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,         
            email TEXT NOT NULL,
            celular TEXT NOT NULL
        )
        """)

        # MESAS
        conn.execute("""
        CREATE TABLE IF NOT EXISTS mesas (
            id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            ubicacion TEXT
        )
        """)

        # HORARIOS
        conn.execute("""
        CREATE TABLE IF NOT EXISTS horarios (
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            descripcion TEXT
        )
        """)

        # RESERVAS
        conn.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_reserva TEXT NOT NULL,
            observacion TEXT,
            cantidad_personas INTEGER,
            id_cliente INTEGER,
            id_mesa INTEGER,
            id_horario INTEGER,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY(id_mesa) REFERENCES mesas(id_mesa),
            FOREIGN KEY(id_horario) REFERENCES horarios(id_horario)
        )
        """)

        conn.commit()