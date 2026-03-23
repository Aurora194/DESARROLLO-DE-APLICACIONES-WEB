# clase gestor de horarios

from .horarios import Horario
#from .bd import init_db, get_db_connection
from conexion.conexion import obtener_conexion

class GestorHorarios:

    # CRUD SQLite
    def agregar_horario(self, horario):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO horarios (hora_inicio, hora_fin, descripcion)
        VALUES (%s,%s,%s)
        """,(
            horario["hora_inicio"],
            horario["hora_fin"],
            horario["descripcion"]
        ))

        conexion.commit()
        conexion.close()

    # listar horarios de tuplas
    def listar_horarios(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM horarios")

        horarios = cursor.fetchall()
        conexion.close()
        return horarios
        
    # Obtener horario por ID
    def obtener_horario(self, id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM horarios WHERE id_horario=%s", (id,)
        )

        horarios = cursor.fetchone()
        conexion.close()
        return horarios
    

    # Actualizar horario
    def actualizar_horario(self, id, horario):
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE horarios
        SET hora_inicio=%s, hora_fin=%s, descripcion=%s
        WHERE id_horario=%s
        """ 
        valores =(
                horario["hora_inicio"],
                horario["hora_fin"],
                horario["descripcion"],
                id
        )
            
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()


    # Eliminar horario
    def eliminar_horario(self, id):

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM horarios WHERE id_horario=%s",
            (id,)
        )

        conexion.commit()
        conexion.close()