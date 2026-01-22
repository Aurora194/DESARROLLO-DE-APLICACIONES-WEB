// Arreglo de productos
let productos = [
    {
        nombre: "Cuaderno",
        precio: 2.60,
        descripcion: "Cuaderno universitario de 100 hojas"
    },
    {
        nombre: "Lápiz",
        precio: 0.80,
        descripcion: "Lápiz de grafito HB"
    },
    {
        nombre: "Mochila",
        precio: 15.00,
        descripcion: "Mochila resistente para uso diario"
    }
];

// Referencia al elemento UL
const lista = document.getElementById("listaProductos");

// Función para renderizar los productos
function mostrarProductos() {
    lista.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            <span class="precio">$${producto.precio.toFixed(2)}</span><br>
            <small>${producto.descripcion}</small>
        `;
        lista.appendChild(li);
    });
}

// Botón para agregar un nuevo producto
document.getElementById("btnAgregar").addEventListener("click", () => {
    const nuevoProducto = {
        nombre: "Producto Nuevo",
        precio: 10.00,
        descripcion: "Descripción del nuevo producto"
    };

    productos.push(nuevoProducto);
    mostrarProductos();
});

// Cargar productos al iniciar la página
mostrarProductos();
