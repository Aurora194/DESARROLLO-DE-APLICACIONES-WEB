const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");
const enviar = document.getElementById("enviar");
const formulario = document.getElementById("registroForm");

function mostrarError(input, mensaje) {
    input.classList.add("invalido");
    input.classList.remove("valido");
    input.nextElementSibling.textContent = mensaje;
}

function mostrarExito(input) {
    input.classList.add("valido");
    input.classList.remove("invalido");
    input.nextElementSibling.textContent = "";
}

function validarNombre() {
    if (nombre.value.length >= 3) {
        mostrarExito(nombre);
        return true;
    } else {
        mostrarError(nombre, "El nombre debe tener al menos 3 caracteres");
        return false;
    }
}

function validarCorreo() {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (regex.test(correo.value)) {
        mostrarExito(correo);
        return true;
    } else {
        mostrarError(correo, "Correo electrónico no válido");
        return false;
    }
}

function validarPassword() {
    const regex = /^(?=.*[0-9])(?=.*[\W]).{8,}$/;
    if (regex.test(password.value)) {
        mostrarExito(password);
        return true;
    } else {
        mostrarError(password, "Mínimo 8 caracteres, un número y un carácter especial");
        return false;
    }
}

function validarConfirmacion() {
    if (confirmar.value === password.value && confirmar.value !== "") {
        mostrarExito(confirmar);
        return true;
    } else {
        mostrarError(confirmar, "Las contraseñas no coinciden");
        return false;
    }
}

function validarEdad() {
    if (edad.value >= 18) {
        mostrarExito(edad);
        return true;
    } else {
        mostrarError(edad, "Debe ser mayor o igual a 18 años");
        return false;
    }
}

function validarFormulario() {
    if (
        validarNombre() &&
        validarCorreo() &&
        validarPassword() &&
        validarConfirmacion() &&
        validarEdad()
    ) {
        enviar.disabled = false;
    } else {
        enviar.disabled = true;
    }
}

nombre.addEventListener("input", validarFormulario);
correo.addEventListener("input", validarFormulario);
password.addEventListener("input", validarFormulario);
confirmar.addEventListener("input", validarFormulario);
edad.addEventListener("input", validarFormulario);

formulario.addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Formulario enviado correctamente ✅");
    formulario.reset();
    enviar.disabled = true;
});
