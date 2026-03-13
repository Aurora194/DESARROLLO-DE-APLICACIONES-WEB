# clase cliente
   
class Cliente:

    def __init__(self, id_cliente, nombre, apellido, email, celular):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.celular = celular


   # tuple
    def to_tuple(self):
        return (self.id_cliente, self.nombre, self.apellido, self.email, self.celular)

    # dict
    def to_dict(self):
        return {
            "id": self.id_cliente,
            "nombre": self.nombre,
            "apellido":self.apellido,
            "email": self.email,
            "celular": self.celular,
        }