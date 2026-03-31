# formulario de cliente

from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp



class ClienteForm(FlaskForm):

    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=200)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField("Email",  validators=[DataRequired(), Email(), Length(max=200)])
    celular = StringField(
        "Celular",
        validators=[
            DataRequired(),
            Regexp(r'^\d{10}$', message="El celular debe tener exactamente 10 números")
        ]
    )


    submit = SubmitField("Guardar Cliente")