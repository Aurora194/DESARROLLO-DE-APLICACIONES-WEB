from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return "Bienvenido al Sistema de Reservas – Restaurante Leña Steak House"

# Ruta dinámica
@app.route('/reserva/<cliente>')
def reserva(cliente):
    return f"Hola {cliente}, tu reserva está en proceso."

# Otra ruta opcional
@app.route('/mesa/<int:numero>')
def mesa(numero):
    return f"Mesa {numero} disponible para reservar."

if __name__ == '__main__':
    app.run(debug=True)


