# formulario de reserva

from flask_wtf import FlaskForm
from wtforms import SelectField,DateField,IntegerField,StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import date


class ReservaForm(FlaskForm):


    # Campo con calendario automático
    fecha_reserva = DateField(
        "Fecha Reserva",
        validators=[DataRequired()],
        format='%Y-%m-%d',
        render_kw={"min":date.today()}
    )

    # Lista desplegable dinámica
    personas = SelectField(
        "Personas",
        choices=[(0, "Seleccione")] + [(i, str(i)) for i in range(1, 9)],
        coerce=int,
        validators=[DataRequired()]
    )

    observacion = StringField("Observación")
    
    id_cliente = SelectField("Cliente",coerce=int)

    id_mesa = SelectField("Mesa",coerce=int)

    id_horario = SelectField("Horario",coerce=int)

    submit = SubmitField("Guardar Reserva")
