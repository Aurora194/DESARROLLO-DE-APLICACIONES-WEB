# clase gestor de clientes

import json
import csv
from .bd import get_db_connection
from pathlib import Path

BASE_PATH = Path(__file__).parent / "data"
TXT_PATH = BASE_PATH / "datos.txt"
JSON_PATH = BASE_PATH / "datos.json"
CSV_PATH = BASE_PATH / "datos.csv"


class GestorClientes:


    # CRUD SQLite

    def agregar_cliente(self, cliente):
        with get_db_connection() as conn:
            conn.execute("""
                INSERT INTO clientes (nombre, email, celular, fecha_reserva, personas)
                VALUES (?, ?, ?, ?, ?)
            """, (
                cliente["nombre"],
                cliente["email"],
                cliente["celular"],
                cliente["fecha_reserva"],
                cliente["personas"]
            ))
            conn.commit()

    # listar clientes de tuplas
    def listar_clientes(self):
        with get_db_connection() as conn:
            return conn.execute("SELECT * FROM clientes").fetchall()

    # obtener cliente por id  ← NUEVO
    def obtener_cliente_por_id(self, id):
        with get_db_connection() as conn:
            return conn.execute(
                "SELECT * FROM clientes WHERE id=?",
                (id,)
            ).fetchone()
        
    # buscar cliente
    def buscar_cliente(self, texto):
        with get_db_connection() as conn:
            return conn.execute(
                "SELECT * FROM clientes WHERE nombre LIKE ?",
                ('%' + texto + '%',)
            ).fetchall()
        

    # actualizar el cliente en la base de datos
    def actualizar_cliente(self, id, cliente):
        with get_db_connection() as conn:
            conn.execute("""
                UPDATE clientes
                SET nombre=?, email=?, celular=?, fecha_reserva=?, personas=?
                WHERE id=?
            """, (
                cliente["nombre"],
                cliente["email"],
                cliente["celular"],
                cliente["fecha_reserva"],
                cliente["personas"],
                id
            ))
            conn.commit()

    # eliminar cliente
    def eliminar_cliente(self, id):
        with get_db_connection() as conn:
            conn.execute("DELETE FROM clientes WHERE id=?", (id,))
            conn.commit()


    # Persistencia TXT

    def guardar_txt(self, cliente):
        with open(TXT_PATH, "a", encoding="utf-8") as f:
            f.write(f"{cliente}\n")

    def leer_txt(self):
        if TXT_PATH.exists():
            with open(TXT_PATH, "r", encoding="utf-8") as f:
                return f.readlines()
        return []


    # Persistencia JSON

    def guardar_json(self, cliente):
        datos = []
        if JSON_PATH.exists():
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                try:
                    datos = json.load(f)
                except:
                    datos = []

        datos.append(cliente)

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    def leer_json(self):
        if JSON_PATH.exists():
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


    # Persistencia CSV

    def guardar_csv(self, cliente):
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                cliente["nombre"],
                cliente["email"],
                cliente["celular"],
                cliente["fecha_reserva"],
                cliente["personas"]
            ])

    def leer_csv(self):
        datos = []
        if CSV_PATH.exists():
            with open(CSV_PATH, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for fila in reader:
                    datos.append(fila)
        return datos