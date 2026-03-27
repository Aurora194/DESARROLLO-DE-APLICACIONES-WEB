from flask import Flask, render_template, redirect, url_for, request, flash
from form_cliente import ClienteForm
from form_reserva import ReservaForm
from datetime import datetime
from reservas.bd import init_db, get_db_connection
from reservas.gestor_clientes import GestorClientes
from reservas.gestor_reservas import GestorReservas
from reservas.gestor_mesas import GestorMesas
from reservas.gestor_horarios import GestorHorarios
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from reservas.models import Usuario
from reservas.gestor_persistencia import (
    guardar_txt, leer_txt,
    guardar_json, leer_json,
    guardar_csv, leer_csv
)
from conexion.conexion import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
from flask import send_file


# FUNCIÓN PARA GENERAR PDF
def generar_pdf(titulo, encabezados, datos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []

    estilos = getSampleStyleSheet()

    # LOGO 
    try:
        logo = Image("static/img/logo.png", width=2*inch, height=2*inch)
        logo.hAlign = 'CENTER'   # centrar logo
        elementos.append(logo)
    except:
        pass
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph(" Restaurante Leña Steak House", estilos["Title"]))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph(titulo, estilos["Heading2"]))
    elementos.append(Spacer(1, 20))

    tabla_data = [encabezados] + datos

    tabla = Table(tabla_data)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    gestor_horarios = GestorHorarios()

    elementos.append(tabla)

    doc.build(elementos)
    buffer.seek(0)

    return buffer


# CONFIGURACIÓN DE LA APLICACIÓN

app = Flask(__name__)

# Clave secreta para formularios Flask-WTF
app.config['SECRET_KEY'] = 'mi_clave_secreta'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reserva.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy (app)

# Inicializar base de datos
#init_db()

#Inicializa Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

login_manager.login_message = "⚠️ Debes iniciar sesión para acceder a esta página"
login_manager.login_message_category = "warning"

# Crear gestores
gestor_clientes = GestorClientes()
gestor_reservas = GestorReservas()
gestor_mesas = GestorMesas()
gestor_horarios = GestorHorarios()


# PÁGINAS PRINCIPALES

# Página de inicio
@app.route('/index')
def inicio():
    return render_template("index.html")


# Página sobre el restaurante
@app.route('/about')
def about():
    return render_template("about.html")

# Pagina contacto
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

# Página calendario reservas
@app.route("/calendario")
def calendario():
    reservas = gestor_reservas.listar_reservas()

    return render_template(
        "calendario.html",
        reservas=reservas
    )

# Panel administrativo
@app.route('/admin')
@login_required
def admin():

    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("login"))

    total_reservas = len(gestor_reservas.listar_reservas())
    total_clientes = len(gestor_clientes.listar_clientes())

    return render_template(
        "admin.html",
        total_reservas=total_reservas,
        total_clientes=total_clientes
    )

# Página menú
@app.route("/menu")
def menu():
    return render_template("menu.html")

# CRUD CLIENTES

# Listar clientes
@app.route("/clientes")
@login_required
def clientes_listar():

    clientes = gestor_clientes.listar_clientes()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# Crear cliente
@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def cliente_nuevo():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "apellido": form.apellido.data,
            "email": form.email.data,
            "celular": form.celular.data
        }

        # Guardar en base de datos
        gestor_clientes.agregar_cliente(cliente)

        # Guardar persistencia archivos
        guardar_txt(str(cliente))
        guardar_json(cliente)
        guardar_csv(cliente)

        flash("Cliente registrado correctamente", "success")

        return redirect(url_for("clientes_listar"))

    return render_template(
        "cliente_form.html",
        form=form
    )


# Editar cliente
@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    cliente = gestor_clientes.obtener_cliente_por_id(id)

    if not cliente:
        flash("Cliente no encontrado", "danger")
        return redirect(url_for("clientes_listar"))

    form = ClienteForm(data={
    "nombre": cliente["nombre"],
    "apellido": cliente["apellido"],
    "email": cliente["email"],
    "celular": cliente["celular"]
})

    if form.validate_on_submit():

        cliente_actualizado = {
            "nombre": form.nombre.data,
            "apellido": form.apellido.data,
            "email": form.email.data,
            "celular": form.celular.data
        }

        gestor_clientes.actualizar_cliente(id, cliente_actualizado)

        flash("Cliente actualizado", "success")

        return redirect(url_for("clientes_listar"))

    return render_template(
        "editar_cliente.html",
        form=form
    )


# Eliminar cliente
@app.route("/clientes/eliminar/<int:id>")
@login_required
def eliminar_cliente(id):

    gestor_clientes.eliminar_cliente(id)

    flash("Cliente eliminado", "warning")

    return redirect(url_for("clientes_listar"))


# Ruta PDF Clientes
@app.route("/clientes/pdf")
@login_required
def pdf_clientes():

    clientes = gestor_clientes.listar_clientes()

    datos = [
        [c["id_cliente"], c["nombre"], c["apellido"], c["email"], c["celular"]]
        for c in clientes
    ]

    pdf = generar_pdf(
        "Listado de Clientes",
        ["ID","Nombre","Apellido","Email","Celular"],
        datos
    )

    return send_file(pdf, download_name="Clientes.pdf", as_attachment=True)

# Ruta por rango ID
@app.route("/clientes/pdf_rango", methods=["GET", "POST"])
@login_required
def pdf_clientes_rango():

    if request.method == "POST":
        inicio = int(request.form.get("inicio"))
        fin = int(request.form.get("fin"))
    else:
        return redirect(url_for("clientes_listar"))  # evita error

    clientes = gestor_clientes.listar_clientes()

    filtrados = [c for c in clientes if inicio <= c["id_cliente"] <= fin]

    datos = [
        [c["id_cliente"], c["nombre"], c["apellido"], c["email"], c["celular"]]
        for c in filtrados
    ]

    pdf = generar_pdf(
        f"Clientes ID {inicio} - {fin}",
        ["ID","Nombre","Apellido","Email","Celular"],
        datos
    )

    return send_file(pdf, download_name="Clientes_Rango.pdf", as_attachment=True)


# CRUD RESERVAS

# Listar reservas
@app.route("/reservas")
@login_required
def reservas():

    reservas = gestor_reservas.listar_reservas()

    return render_template(
        "reservas.html",
        reservas=reservas
    )


# Crear reserva
@app.route("/reservas/nuevo", methods=["GET", "POST"])
@login_required
def reserva_nuevo():

    form = ReservaForm()

    # llenar listas dinámicas
    form.id_cliente.choices = [(0,"Seleccione")] + [
        (c["id_cliente"], f'{c["nombre"]} {c["apellido"]}')
        for c in gestor_clientes.listar_clientes()
    ]

    form.id_mesa.choices = [(0,"Seleccione")] + [
        (m["id_mesa"], m["nombre"])
        for m in gestor_mesas.listar_mesas()
    ]

    form.id_horario.choices = [(0,"Seleccione")] + [
        (h["id_horario"], h["descripcion"])
        for h in gestor_horarios.listar_horarios()
    ]

    if request.method == "POST":

        reserva = {
            "fecha_reserva": str(form.fecha_reserva.data),
            "personas": form.personas.data,
            "observacion": form.observacion.data,
            "id_cliente": form.id_cliente.data,
            "id_mesa": form.id_mesa.data,
            "id_horario": form.id_horario.data
        }

        gestor_reservas.agregar_reserva(reserva)

        flash("Reserva registrada correctamente","success")

        return redirect(url_for("reservas"))

    return render_template("reserva_form.html", form=form)


# Editar reserva
@app.route("/reservas/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar_reserva(id):

    reserva = gestor_reservas.obtener_reserva(id)

    if not reserva:
        flash("Reserva no encontrada", "danger")
        return redirect(url_for("reservas"))

    form = ReservaForm()

    # llenar listas
    form.id_cliente.choices = [(c["id_cliente"], c["nombre"]) for c in gestor_clientes.listar_clientes()]
    form.id_mesa.choices = [(m["id_mesa"], m["nombre"]) for m in gestor_mesas.listar_mesas()]
    form.id_horario.choices = [(h["id_horario"], h["descripcion"]) for h in gestor_horarios.listar_horarios()]

    if request.method == "POST":

        reserva_actualizada = {
            "fecha_reserva": str(form.fecha_reserva.data),
            "personas": form.personas.data,
            "observacion": form.observacion.data,
            "id_cliente": form.id_cliente.data,
            "id_mesa": form.id_mesa.data,
            "id_horario": form.id_horario.data
        }

        gestor_reservas.actualizar_reserva(id, reserva_actualizada)
        flash("Reserva actualizada correctamente", "success")
        return redirect(url_for("reservas"))
    return render_template("editar_reserva.html", form=form, reserva=reserva)


# Eliminar reserva
@app.route("/reservas/eliminar/<int:id>")
@login_required
def eliminar_reserva(id):

        gestor_reservas.eliminar_reserva(id)

        flash("Reserva eliminada", "warning")

        return redirect(url_for("reservas"))


# Ruta PDF Reservas
@app.route("/reservas/pdf")
@login_required
def pdf_reservas():

    reservas = gestor_reservas.listar_reservas()

    datos = [
        [r["id_reserva"], r["fecha_reserva"], r["cantidad_personas"], r["observacion"]]
        for r in reservas
    ]

    pdf = generar_pdf(
        "Listado de Reservas",
        ["ID","Fecha","Personas","Observación"],
        datos
    )

    return send_file(pdf, download_name="Reservas.pdf", as_attachment=True)


# Ruta por rango de fechas
@app.route("/reservas/pdf_rango", methods=["GET","POST"])
@login_required
def pdf_reservas_rango():

    inicio = request.form.get("inicio")
    fin = request.form.get("fin")

    reservas = gestor_reservas.listar_reservas()

    filtrados = [
        r for r in reservas
        if inicio <= r["fecha_reserva"] <= fin
    ]

    datos = [
        [r["id_reserva"], r["fecha_reserva"], r["cantidad_personas"], r["observacion"]]
        for r in filtrados
    ]

    pdf = generar_pdf(
        f"Reservas {inicio} a {fin}",
        ["ID","Fecha","Personas","Observación"],
        datos
    )

    return send_file(pdf, download_name="Reservas_Rango.pdf", as_attachment=True)

# MESAS

@app.route("/mesas")
@login_required
def mesas():

    mesas = gestor_mesas.listar_mesas()

    return render_template(
        "mesas.html",
        mesas=mesas
    )

# Crear nueva mesa
@app.route("/mesas/nuevo", methods=["GET", "POST"])
@login_required
def mesa_nueva():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        ubicacion = request.form.get("ubicacion")

        mesa = {
            "nombre": nombre,
            "descripcion": descripcion,
            "ubicacion": ubicacion
        }

        gestor_mesas.agregar_mesa(mesa)

        flash("Mesa creada correctamente", "success")

        return redirect(url_for("mesas"))

    return render_template("mesa_form.html")

# Editar mesa
@app.route("/mesas/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar_mesa(id):

    mesa = gestor_mesas.obtener_mesa(id)
    if request.method == "POST":
        mesa_actualizada = {
            "nombre": request.form.get("nombre"),
            "descripcion": request.form.get("descripcion"),
            "ubicacion": request.form.get("ubicacion")
        }

        gestor_mesas.actualizar_mesa(id, mesa_actualizada)
        flash("Mesa actualizada correctamente","success")
        return redirect(url_for("mesas"))
    return render_template("editar_mesa.html", mesa=mesa)

# Eliminar mesa
@app.route("/mesas/eliminar/<int:id>")
@login_required
def eliminar_mesa(id):

    gestor_mesas.eliminar_mesa(id)
    flash("Mesa eliminada","warning")
    return redirect(url_for("mesas"))

# Ruta Pdf Mesas
@app.route("/mesas/pdf")
@login_required
def pdf_mesas():

    mesas = gestor_mesas.listar_mesas()

    datos = [
        [m["id_mesa"], m["nombre"], m["descripcion"], m["ubicacion"]]
        for m in mesas
    ]

    pdf = generar_pdf(
        "Listado de Mesas",
        ["ID", "Nombre", "Descripción", "Ubicación"],
        datos
    )

    return send_file(pdf, download_name="Mesas.pdf", as_attachment=True)

# Ruta por rango de ID
@app.route("/mesas/pdf_rango", methods=["GET","POST"])
@login_required
def pdf_mesas_rango():

    inicio = int(request.form.get("inicio"))
    fin = int(request.form.get("fin"))

    mesas = gestor_mesas.listar_mesas()

    filtradas = [
        m for m in mesas
        if inicio <= m["id_mesa"] <= fin
    ]

    datos = [
        [m["id_mesa"], m["nombre"], m["descripcion"], m["ubicacion"]]
        for m in filtradas
    ]

    pdf = generar_pdf(
        f"Mesas del ID {inicio} al {fin}",
        ["ID", "Nombre", "Descripción", "Ubicación"],
        datos
    )

    return send_file(pdf, download_name="Mesas_Rango.pdf", as_attachment=True)


# HORARIOS

@app.route("/horarios")
@login_required
def horarios():

    horarios = gestor_horarios.listar_horarios()
    return render_template(
        "horarios.html",
        horarios=horarios
    )

# Crear nuevo horario
@app.route("/horarios/nuevo", methods=["GET", "POST"])
@login_required
def horario_nuevo():

    if request.method == "POST":
        hora_inicio = request.form.get("hora_inicio")
        hora_fin = request.form.get("hora_fin")
        descripcion = request.form.get("descripcion")

        horario = {
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "descripcion": descripcion
        }

        gestor_horarios.agregar_horario(horario)
        flash("Horario creado correctamente", "success")
        return redirect(url_for("horarios"))
    return render_template("horario_form.html")

# Editar horario
@app.route("/horarios/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar_horario(id):

    horario = gestor_horarios.obtener_horario(id)
    if request.method == "POST":
        horario_actualizado = {
            "hora_inicio": request.form.get("hora_inicio"),
            "hora_fin": request.form.get("hora_fin"),
            "descripcion": request.form.get("descripcion")
        }

        gestor_horarios.actualizar_horario(id, horario_actualizado)
        flash("Horario actualizado","success")
        return redirect(url_for("horarios"))
    return render_template("editar_horario.html", horario=horario)

# Eliminar horario
@app.route("/horarios/eliminar/<int:id>")
@login_required
def eliminar_horario(id):

    gestor_horarios.eliminar_horario(id)
    flash("Horario eliminado","warning")
    return redirect(url_for("horarios"))

# Ruta PDF horarios
@app.route("/horarios/pdf")
@login_required
def pdf_horarios():

    horarios = gestor_horarios.listar_horarios()

    datos = [
        [h["id_horario"], h["hora_inicio"], h["hora_fin"], h["descripcion"]]
        for h in horarios
    ]

    pdf = generar_pdf(
        "Listado de Horarios",
        ["ID", "Inicio", "Fin", "Descripción"],
        datos
    )

    return send_file(pdf, download_name="Horarios.pdf", as_attachment=True)

# Ruta por rango ID
@app.route("/horarios/pdf_rango", methods=["GET","POST"])
@login_required
def pdf_horarios_rango():

    inicio = int(request.form.get("inicio"))
    fin = int(request.form.get("fin"))

    horarios = gestor_horarios.listar_horarios()

    filtrados = [
        h for h in horarios
        if inicio <= h["id_horario"] <= fin
    ]

    datos = [
        [h["id_horario"], h["hora_inicio"], h["hora_fin"], h["descripcion"]]
        for h in filtrados
    ]

    pdf = generar_pdf(
        f"Horarios del ID {inicio} al {fin}",
        ["ID", "Inicio", "Fin", "Descripción"],
        datos
    )

    return send_file(pdf, download_name="Horarios_Rango.pdf", as_attachment=True)

# Ruta usuarios
@app.route("/usuarios/nuevo", methods=["GET","POST"])
@login_required
def usuario_nuevo():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        conexion = obtener_conexion()

        if not conexion:
            flash("Error de conexión a MySQL", "danger")
            return redirect(url_for("login"))

        cursor = conexion.cursor(dictionary=True)

        sql = """
        INSERT INTO usuarios (nombre, email, password)
        VALUES (%s, %s, %s)
        """

        password_hash = generate_password_hash(password)

        cursor.execute(sql,(nombre,email,password_hash))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Usuario creado","success")

        return redirect(url_for("usuarios"))

    return render_template("usuario_form.html")

# Consultar ususarios
@app.route("/usuarios")
@login_required
def usuarios():
    
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("inicio"))

    conexion = obtener_conexion()   # 👈 FALTABA

    if not conexion:
        flash("Error de conexión", "danger")
        return redirect(url_for("inicio"))

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE estado='ACTIVO'")
    usuarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("usuarios.html", usuarios=usuarios)

# Actualizar
@app.route("/usuarios/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar_usuario(id):

    conexion = obtener_conexion()

    if not conexion:
        flash("Error de conexión a MySQL", "danger")
        return redirect(url_for("login"))

    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":

        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        sql = """
        UPDATE usuarios
        SET nombre=%s, email=%s, password=%s
        WHERE id_usuario=%s
        """


        password_hash = generate_password_hash(password)
        cursor.execute(sql,(nombre,email,password_hash,id))
        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Usuario actualizado","success")

        return redirect(url_for("usuarios"))

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s",(id,))
    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template("editar_usuario.html", usuario=usuario)

# Eliminar 
@app.route("/usuarios/eliminar/<int:id>")
@login_required
def eliminar_usuario(id):

    conexion = obtener_conexion()

    if not conexion:
        flash("Error de conexión a MySQL", "danger")
        return redirect(url_for("login"))

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("UPDATE usuarios SET estado='ELIMINADO' WHERE id_usuario=%s",(id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Usuario eliminado","warning")

    return redirect(url_for("usuarios"))

# Cargar usuario desde MYSQL
@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()

    if not conexion:
        return None   # ✅ SOLO ESTO

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (int(user_id),))
    user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if user:
        return Usuario(
            user["id_usuario"],
            user["nombre"],
            user["email"],
            user["password"],
            user["rol"]

        )

    return None

# Registro de usuarios
@app.route("/registro", methods=["GET","POST"])
def registro():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        conexion = obtener_conexion()
        if not conexion:
            flash("Error de conexión a la base de datos", "danger")
            return redirect(url_for("login"))

        cursor = conexion.cursor(dictionary=True)

        if not email or not password:
            flash("Complete todos los campos", "warning")
            return redirect(url_for("login"))
        
        # 🔍 Verificar si el correo ya existe
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        existe = cursor.fetchone()

        if existe:
            cursor.close()
            conexion.close()
            flash("El correo ya está registrado", "warning")
            return redirect(url_for("registro"))

        # Encriptar contraseña
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Insertar usuario
        rol = "usuario"

        sql = "INSERT INTO usuarios (nombre,email,password,rol) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql,(nombre,email,password_hash,rol))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Usuario registrado correctamente","success")
        return redirect(url_for("login"))

    return render_template("registro.html")

# Login
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Complete todos los campos", "warning")
            return redirect(url_for("login"))

        conexion = obtener_conexion()
        if not conexion:
            flash("Error de conexión a la base de datos", "danger")
            return redirect(url_for("login"))

        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conexion.close()

        # ✅ TODO dentro del POST
        if user and check_password_hash(user["password"], password):

            usuario = Usuario(
                user["id_usuario"],
                user["nombre"],
                user["email"],
                user["password"],
                user["rol"]
            )

            login_user(usuario)
            flash("Bienvenido " + usuario.nombre, "success")

            if usuario.rol == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("inicio"))

        else:
            flash("Credenciales incorrectas", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Logout cerrar sesión
@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash("Sesión cerrada","info")
    return redirect(url_for("login"))


# PERSISTENCIA ARCHIVOS

@app.route("/datos", methods=["GET", "POST"])
def datos():

    if request.method == 'POST':

        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        celular = request.form.get('celular')

        registro = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "celular": celular
        }

        # Guardar archivos
        guardar_txt(str(registro))
        guardar_json(registro)
        guardar_csv(registro)

        flash("Datos guardados en TXT, JSON y CSV", "success")

        return redirect(url_for('datos'))

    # Leer archivos
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()

    return render_template(
        'datos.html',
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv
    )


# EJECUTAR APLICACIÓN
if __name__ == '__main__':
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)