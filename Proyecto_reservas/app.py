from flask import Flask, render_template, redirect, url_for, request, flash
from form import ClienteForm
from datetime import datetime
from reservas.bd import init_db
from reservas.gestor_clientes import GestorClientes
from flask_sqlalchemy import SQLAlchemy
from reservas.gestor_persistencia import guardar_csv, leer_csv, guardar_json,  leer_json, guardar_txt,  leer_txt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy (app)

init_db()
gestor = GestorClientes()

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/reservas')
def reservas():
    return render_template("reservas.html")

# Ruta dinámica
@app.route('/reservas/<cliente>')
def reserva(cliente):
    return render_template("reservas.html", cliente=cliente)

# ruta de clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def cliente_nuevo():
    form = ClienteForm()

    if form.validate_on_submit():
        cliente = {
            "nombre": form.nombre.data,
            "email": form.email.data,
            "celular": form.celular.data,
            "fecha_reserva": str(form.fecha_reserva.data),
            "personas": form.personas.data
        }

        guardar_txt(str(cliente))
        guardar_json("clientes.json", cliente)
        guardar_csv(cliente.values())

        flash("Reserva registrada correctamente", "success")
        return redirect(url_for("clientes_listar"))
    return render_template("cliente_form.html", form=form)


# ruta para listar clientes 
@app.route("/clientes")
def clientes_listar():
    clientes = gestor.listar_clientes()
    return render_template("clientes.html", clientes=clientes)

# ruta para buscar cliente
@app.route("/clientes/buscar", methods=["GET", "POST"])
def buscar_cliente():
    resultados = []
    if request.method == "POST":
        texto = request.form["texto"]
        resultados = gestor.buscar_cliente(texto)
    return render_template("buscar_cliente.html", resultados=resultados)   

# ruta para editar cliente
@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente_db = gestor.obtener_cliente_por_id(id)

    if not cliente_db:
        flash("Cliente no encontrado", "danger")
        return redirect(url_for("clientes_listar"))

    # Convertir la fecha string a objeto date
    cliente_db = dict(cliente_db)
    cliente_db["fecha_reserva"] = datetime.strptime(
        cliente_db["fecha_reserva"], "%Y-%m-%d"
    ).date()

    form = ClienteForm(data=cliente_db)

    if form.validate_on_submit():
        cliente_actualizado = {
            "nombre": form.nombre.data,
            "email": form.email.data,
            "celular": form.celular.data,
            "fecha_reserva": str(form.fecha_reserva.data),
            "personas": form.personas.data
        }

        gestor.actualizar_cliente(id, cliente_actualizado)

        flash("Reserva actualizada correctamente", "success")
        return redirect(url_for("clientes_listar"))

    return render_template("editar_cliente.html", form=form)

# ruta para eliminar cliente

@app.route("/clientes/eliminar/<int:id>")
def eliminar_cliente(id):
    gestor.eliminar_cliente(id)
    flash("Reserva eliminada", "success")
    return redirect(url_for("clientes_listar"))


# ruta para los datos persistentes
@app.route('/datos')
def datos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        fecha_reserva = request.form.get('fecha_reserva')
        personas = request.form.get ('personas')

   # registrar en base
    dic={
    'nombre': nombre,
    'email': email,
    'celular': celular,
    'fecha_reserva': fecha_reserva,
    'personas': personas
    }

    # guardar en 3 formatos
    guardar_txt(f" ({nombre},  {email},  {celular}, {fecha_reserva}, {personas}")
    guardar_json(dic)
    guardar_csv(dic.values())
    flash('Datos guardados exitosamente', 'success')
    return redirect(url_for('datos'))
   
    # leer datos de los 3 formatos
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_cvs = leer_csv()
    return render_template('datos.html', datos_txt=datos_txt, datos_json=datos_json, datos_csv=datos_cvs)


if __name__ == '__main__':
            app.run(debug=True)
