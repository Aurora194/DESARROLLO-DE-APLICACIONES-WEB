# clase gestor de reservas

from .reservas import Reserva
from .bd import init_db, get_db_connection
from conexion.conexion import obtener_conexion

class GestorReservas:
        

    # CRUD SQLite

    def agregar_reserva(self, reserva):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO reservas(
        fecha_reserva,
        cantidad_personas,
        observacion,
        id_cliente,
        id_mesa,
        id_horario
        )
        VALUES(%s,%s,%s,%s,%s,%s)
        """,(
            reserva["fecha_reserva"],
            reserva["personas"],
            reserva["observacion"],
            reserva["id_cliente"],
            reserva["id_mesa"],
            reserva["id_horario"]
        ))

        conexion.commit()
        conexion.close()
            
    # listar reservas de tuplas
    def listar_reservas(self):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT r.id_reserva,
                r.fecha_reserva,
                r.cantidad_personas,
                r.observacion,
                c.nombre AS cliente,
                m.nombre AS mesa,
                h.descripcion AS horario
            FROM reservas r
            JOIN clientes c ON r.id_cliente = c.id_cliente
            JOIN mesas m ON r.id_mesa = m.id_mesa
            JOIN horarios h ON r.id_horario = h.id_horario
            ORDER BY r.fecha_reserva
        """)

        reservas = cursor.fetchall()   # 👈 FALTABA ESTO

        cursor.close()
        conexion.close()

        return reservas


    # obtener reserva por id  
    def obtener_reserva(self,id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM reservas WHERE id_reserva=%s", (id,)
        )

        reserva = cursor.fetchone()
        conexion.close()
        return reserva
        

    # actualizar la reserva en la base de datos
    def actualizar_reserva(self, id, reserva):

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE reservas
        SET fecha_reserva=%s,
            cantidad_personas=%s,
            observacion=%s,
            id_cliente=%s,
            id_mesa=%s,
            id_horario=%s
        WHERE id_reserva=%s
        """

        valores = (reserva["fecha_reserva"],
                reserva["personas"],
                reserva["observacion"],
                reserva["id_cliente"],
                reserva["id_mesa"],
                reserva["id_horario"],
                id
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()


    # eliminar reserva
    def eliminar_reserva(self,id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM reservas WHERE id_reserva=%s",
            (id,)
        )

        conexion.commit()
        conexion.close()


    # buscar reserva
    def buscar_reserva(self, cliente):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT r.id_reserva,
                r.fecha_reserva,
                r.cantidad_personas,
                r.observacion,
                c.nombre AS cliente,
                m.nombre AS mesa,
                h.descripcion AS horario
            FROM reservas r
            JOIN clientes c ON r.id_cliente = c.id_cliente
            JOIN mesas m ON r.id_mesa = m.id_mesa
            JOIN horarios h ON r.id_horario = h.id_horario
            WHERE c.nombre LIKE %s
        """, ('%' + cliente + '%',))

        reservas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return reservas