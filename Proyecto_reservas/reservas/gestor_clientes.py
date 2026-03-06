# clase gestor de clientes 

from .clientes import Cliente
from .bd import init_db, get_db_connection


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

    # obtener cliente por id  
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
