# clase cliente
   
class Cliente:
    def __init__(self, id, nombre, email, celular, fecha_reserva, personas):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.fecha_reserva = fecha_reserva
        self.personas = personas

   # tuple
    def to_tuple(self):
        return (self.id, self.nombre, self.email, self.celular, self.fecha_reserva, self.personas)

    # dict
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "celular": self.celular,
            "fecha_reserva": self.fecha_reserva,
            "personas": self.personas
        }