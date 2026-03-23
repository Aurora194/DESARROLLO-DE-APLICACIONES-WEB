# clase gestor de clientes 

from .horarios import Horario
#from .bd import init_db, get_db_connection
from conexion.conexion import obtener_conexion


class GestorClientes:


    # CRUD SQLite

    def agregar_cliente(cliente):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO clientes (nombre, apellido, email, celular)
        VALUES (%s,%s,%s,%s)
        """

        valores = (
            cliente["nombre"],
            cliente["apellido"],
            cliente["email"],
            cliente["celular"]
        )

        cursor.execute(sql, valores)

        conexion.commit()
        conexion.close()

    # listar clientes 
    def listar_clientes(self):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conexion.close()
        return clientes


    # obtener cliente por id  
    def obtener_cliente_por_id(self, id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM clientes WHERE id_cliente=%s", (id,)
        )

        cliente = cursor.fetchone()
        conexion.close()
        return cliente
        
    # buscar cliente
    def buscar_cliente(self, texto):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql = "SELECT * FROM clientes WHERE nombre LIKE %s"
        cursor.execute(sql, ("%" + texto + "%",))

        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()

        return resultados

    # actualizar el cliente en la base de datos
    def actualizar_cliente(self, id, cliente):

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE clientes
        SET nombre=%s, apellido=%s, email=%s, celular=%s
        WHERE id_cliente=%s
        """

        valores = (
            cliente["nombre"],
            cliente["apellido"],
            cliente["email"],
            cliente["celular"],
            id
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()


    # eliminar cliente
    def eliminar_cliente(self, id):

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM clientes WHERE id_cliente=%s",
            (id,)
        )

        conexion.commit()
        conexion.close()