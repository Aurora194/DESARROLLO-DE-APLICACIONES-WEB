# clase reserva

class Reserva:

    def __init__(self,id,fecha_reserva,personas,observacion,id_cliente,id_mesa,id_horario):

        self.id=id
        self.fecha_reserva=fecha_reserva
        self.personas=personas
        self.observacion=observacion
        self.id_cliente=id_cliente
        self.id_mesa=id_mesa
        self.id_horario=id_horario

     # tuple
    def to_tuple(self):
        return (self.id, self.fecha_reserva, self.personas, self.observacion, self.id_cliente, self.id_mesa,self.id_horario)


    # dict
    def to_dict(self):

        return {
            "id":self.id,
            "fecha_reserva":self.fecha_reserva,
            "personas":self.personas,
            "observacion":self.observacion,
            "id_cliente":self.id_cliente,
            "id_mesa":self.id_mesa,
            "id_horario":self.id_horario
        }
   