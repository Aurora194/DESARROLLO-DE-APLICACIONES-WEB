# conexion a mysql
import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='reservas_restaurante',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None