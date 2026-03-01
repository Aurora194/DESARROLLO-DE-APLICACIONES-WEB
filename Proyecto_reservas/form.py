# formulario de producto

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[DataRequired(), Length (min=2, max=200)])
    descripcion = StringField('Descripción del producto', validators=[DataRequired(), Length(min=2, max=500)])
    cantidad = DecimalField('Cantidad disponible', validators=[DataRequired(), NumberRange (min=0)], places = 0)
    precio = DecimalField('Precio del producto', validators=[DataRequired(), NumberRange (min=0.00)], places=2)
    submit= SubmitField('Agregar Producto')