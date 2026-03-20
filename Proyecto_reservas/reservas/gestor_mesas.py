# clase gestor de mesas 

from .mesas import Mesa
from .bd import init_db, get_db_connection
from conexion.conexion import obtener_conexion

class GestorMesas:

    # CRUD SQLite
    def agregar_mesa(self, mesa):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO mesas (nombre, descripcion, ubicacion)
        VALUES (%s,%s,%s)
        """,(
            mesa["nombre"],
            mesa["descripcion"],
            mesa["ubicacion"]
        ))

        conexion.commit()
        conexion.close()

    # listar mesas de tuplas
    def listar_mesas(self):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mesas")
        mesas = cursor.fetchall()
        conexion.close()

        return mesas
        
  # Obtener una mesa por ID
    def obtener_mesa(self, id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM mesas WHERE id_mesa=%s", (id,)
        )

        mesas = cursor.fetchone()
        conexion.close()
        return mesas
    
    # Actualizar mesa
    def actualizar_mesa(self, id, mesa):

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE mesas
        SET nombre=%s, descripcion=%s, ubicacion=%s
        WHERE id_mesa=%s
        """

        valores = (
                mesa["nombre"],
                mesa["descripcion"],
                mesa["ubicacion"],
            id
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

    # Eliminar mesa
    def eliminar_mesa(self, id):

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM mesas WHERE id_mesa=%s",
            (id,)
        )

        conexion.commit()
        conexion.close()