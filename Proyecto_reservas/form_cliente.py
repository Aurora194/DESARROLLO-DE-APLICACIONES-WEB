# formulario de cliente

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from datetime import date


class ClienteForm(FlaskForm):

    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=200)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField("Email",  validators=[DataRequired(), Email(), Length(max=200)])
    celular = StringField("Celular", validators=[DataRequired(), Length(min=10, max=10)])



    submit = SubmitField("Guardar Cliente")