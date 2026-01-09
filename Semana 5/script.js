const gallery = document.getElementById("gallery");
const addBtn = document.getElementById("addBtn");
const deleteBtn = document.getElementById("deleteBtn");
const imageUrl = document.getElementById("imageUrl");


let selectedImage = null;


// Agregar imagen
addBtn.addEventListener("click", () => {
const url = imageUrl.value.trim();
if (!url) return alert("Ingrese una URL válida");


const img = document.createElement("img");
img.src = url;


img.addEventListener("click", () => selectImage(img));


gallery.appendChild(img);
imageUrl.value = "";
});

// Seleccionar imagen
function selectImage(img) {
if (selectedImage) {
selectedImage.classList.remove("selected");
}
selectedImage = img;
img.classList.add("selected");
}


// Eliminar imagen seleccionada


deleteBtn.addEventListener("click", () => {
if (!selectedImage) return alert("No hay imagen seleccionada");
selectedImage.remove();
selectedImage = null;
});

// Atajo teclado eliminar con Supr


document.addEventListener("keydown", (e) => {
if (e.key === "Delete" && selectedImage) {
selectedImage.remove();
selectedImage = null;
}
});