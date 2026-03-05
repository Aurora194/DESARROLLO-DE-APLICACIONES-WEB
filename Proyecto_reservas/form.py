# formulario de cliente

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from datetime import date


class ClienteForm(FlaskForm):

    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField("Email",  validators=[DataRequired(), Email(), Length(max=200)])
    celular = StringField("Celular", validators=[DataRequired(), Length(min=10, max=10)])

    # Campo con calendario automático
    fecha_reserva = DateField(
        "Fecha de Reserva",
        validators=[DataRequired()],
        format='%Y-%m-%d',
        render_kw={"min": date.today()}  # No permite fechas pasadas
    )

    # Lista desplegable dinámica
    personas = SelectField(
    "Número de Personas",
    choices=[(0, "")] + [(i, f"{i} Persona" if i == 1 else f"{i} Personas") for i in range(1, 9)],
    coerce=int,
    validators=[DataRequired()]
)

    submit = SubmitField("Guardar Reserva")