# clase reservas
from .clientes import Cliente
from .bd import init_db, get_db_connection

class Inventario:
    def __init__(self):
        self.productos = {} 
        self.nombres = set()

    def cargar_desde_db(self):
        with get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM productos')
            for row in cursor.fetchall():
                producto = Producto (row['id'], row['nombre'], row['descripcion'], row['cantidad'], row['precio'])
                self.productos [producto.id] = producto
                self.nombres.add(producto.nombre)

    # listar productos de tuplas
    def listar_productos (self):
        return [producto.to_tuple() for producto in self.productos.values()]
    
    # buscar por nombre |
    def buscar_por_nombre (self, texto):
        texto = texto.lower().strip()
        resultados = []
        for producto in self.productos.values():
            if texto in producto.nombre.lower() or texto in producto.descripcion.lower():
                resultados.append(producto.to_tuple())
        return resultados

    # agregar producto
    def agregar_producto (self, nombre, descripcion, cantidad, precio):
        cantidad= int(cantidad)
        precio = float(precio)
        with get_db_connection() as conn:
            cursor = conn.execute('INSERT INTO productos (nombre, descripcion, cantidad, precio) VALUES (?, ?, ?, ?)',
                                (nombre, descripcion, cantidad, precio))
            conn.commit()
            nuevo_id = cursor.lastrowid
            nuevo_producto = Producto (nuevo_id, nombre, descripcion, cantidad, precio)
            self.productos [nuevo_id] = nuevo_producto
            self.nombres.add(nombre)

    # actualizar el producto en la base de datos
    def actualizar_producto (self, id, nombre, descripcion, cantidad, precio):
        cantidad= int(cantidad)
        precio = float(precio)
        if id in self.productos:
            with get_db_connection() as conn:
                conn.execute('UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ? WHERE id = ?',
                            (nombre, descripcion, cantidad, precio, id))
                conn.commit()
                producto = self.productos[id]
                self.nombres.discard (producto.nombre)
                producto.nombre = nombre
                producto.descripcion = descripcion
                producto.cantidad = cantidad
                producto.precio = precio
                self.nombres.add(nombre)
                conn.commit()

    # eliminar producto
    def eliminar_producto (self, id):
        if id in self.productos:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM productos WHERE id = ?', (id,))
                conn.commit()
                producto = self.productos.pop(id)
                self.nombres.discard (producto.nombre)
