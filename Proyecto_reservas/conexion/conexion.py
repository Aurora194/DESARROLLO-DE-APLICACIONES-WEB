# conexion a mysql
import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3308,
            database='reservas_restaurante',
            user='root',
            password='12345'
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("ERROR MYSQL:", e)
        return None