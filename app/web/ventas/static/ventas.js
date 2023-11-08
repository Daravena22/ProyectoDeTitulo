productos = {}
carrito_productos = {}

const agregarVenta = async () => {
  response = await fetch(`/api/clientes/listartodo`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  rowData = await response.json();
  const listadocliente = document.getElementById('cliente');
    listadocliente.innerHTML = "";
    rowData.data.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre + ' ' + item.apellido;
      listadocliente.appendChild(option);
    });

    response = await fetch(`/api/productos/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    rowData = await response.json();
    const listadoproducto = document.getElementById('productos');
    listadoproducto.innerHTML = "";
    productos = {}
    rowData.data.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre + '-' + item.detalle;
      listadoproducto.appendChild(option);

      productos [item.id] = {precio:item.precio, stock:item.stock}
    });   
     console.log(productos)
     $('#precio').val(rowData.data[0].precio);
     $('#cantidad').val(1)
     calcular_total()
  $('#AgregarVentaModal').modal('toggle');
};

function seleccionar_producto(id_producto) {
  id_producto = id_producto.value
  console.log(id_producto)
 var precio = productos[id_producto].precio;
 console.log(precio)
 $('#precio').val(precio);
 $('#cantidad').val(1)
 calcular_total();
}

function calcular_total() {
 
  precio = document.getElementById('precio').value
  cantidad = document.getElementById('cantidad').value
 $('#precio').val(precio);
 $('#total').val(precio*cantidad);
}

function agregar_producto(){

id_producto = document.getElementById('productos').value
if(carrito_productos[id_producto] !== undefined){
  return
}
  
indice = document.getElementById('productos').selectedIndex  
producto = document.getElementById('productos').options[indice].text 
precio = document.getElementById('precio').value
cantidad = document.getElementById('cantidad').value
var carrito = document.getElementById("carrito");

fila = carrito.insertRow();
celda = fila.insertCell();
celda.innerHTML = producto;

celda = fila.insertCell();
celda.innerHTML = cantidad;

celda = fila.insertCell();
celda.innerHTML = precio;

celda = fila.insertCell();
celda.innerHTML = cantidad*precio;

console.log(fila)
carrito_productos[id_producto] = {precio:precio, cantidad:cantidad}
}