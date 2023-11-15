productos = {}
carrito_productos = {}
total = 0

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

  response = await fetch(`/api/mantenedores/tipo_abono/listartodo`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  rowData = await response.json();
  const listado_tipo_abono = document.getElementById('tipo_abono');
  listado_tipo_abono.innerHTML = "";
  rowData.data.forEach(item => {
    const option = document.createElement('option');
    option.value = item.id;
    option.textContent = item.nombre;
    listado_tipo_abono.appendChild(option);
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

    productos[item.id] = { precio: item.precio, stock: item.stock }
  });
  console.log(productos)
  $('#precio').val(rowData.data[0].precio);
  $('#cantidad').val(1)
  calcular_total()
  total = 0
  $('#monto_neto').val(0);
  $('#monto_bruto').val(0);
  $('#abonar').val(0);
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
  $('#total').val(precio * cantidad);
}

function agregar_producto() {

  id_producto = document.getElementById('productos').value
  if (carrito_productos[id_producto] !== undefined) {
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
  celda.innerHTML = cantidad * precio;

  console.log(fila)
  carrito_productos[id_producto] = { precio: precio, cantidad: cantidad }

  total = total + cantidad * precio
  $('#monto_neto').val(total);
  $('#monto_bruto').val(total * 1.19);

}



const agregar_venta = async () => {

  lugar = document.getElementById('lugar').value
  fecha = document.getElementById('fecha').value
  cliente = document.getElementById('cliente').value
  abonado = document.getElementById('abonar').value
  tipo_abono = document.getElementById('tipo_abono').value

  const response = await fetch('/api/ventas/agregar', {
    method: 'PUT',
    body: JSON.stringify({ lugar: lugar, fecha: fecha, cliente: cliente, carrito: carrito_productos, abonado: abonado, tipo_abono: tipo_abono }), // string or object
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const myJson = await response.json();
  $('#lugar').val('')
  $('#fecha').val('')
  $('#cliente').val('')

  $('#datos_venta').DataTable().ajax.reload();
  $('#AgregarVentaModal').modal('toggle')
  toastr.success('Venta guardada exitosamente')

}
$(document).ready(function () {
  $('#datos_venta').DataTable({
    "processing": true,
    serverSide: true,
    ajax: {
      url: '/api/ventas/listar',
      type: 'GET',

    },
    columns: [

      { data: 'folio', title: 'FOLIO' },
      { data: 'cliente', title: 'CLIENTE' },
      { data: 'fecha', title: 'FECHA' },
      { data: 'total', title: 'TOTAL' },
      { data: 'abonado', title: 'ABONADO' },


      // {
      //   data: null, title: "ACCIONES",
      //   render: function (data, type, row) {
      //     return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarProducto(' + row.id + ')">Eliminar</button>' +
      //       '<button type="button" class="btn btn-primary editar-btn" onclick="editarProducto(' + row.id + ')">Editar</button>';
      //   }
      // }

      // Configura tus columnas aquí

    ],
    "language": {
      "lengthMenu": "Mostrar _MENU_ registros por página",
      "zeroRecords": "No se han encontrado Clientes",
      "info": "Mostrando página _PAGE_ de _PAGES_",
      "search": "Buscar Venta",
      "infoEmpty": "No hay registros disponibles",
      "infoFiltered": "(filtrados de _MAX_ registros totales)",
      "paginate":{
        "first": "Primero",
         "last" : "Ültimo",
         "next": "Siguiente",
         "previous": "Anterior"
      }
    }
  });
});


function agregar_venta_sgte_pestana() {
  if (document.getElementById('datos-tab').classList.contains('active')) {
    document.getElementById('datos-tab').classList.remove('active');
    document.getElementById('productos-tab').classList.add('active');
    document.getElementById('datos-tab-pane').classList.remove('show', 'active');
    document.getElementById('productos-tab-pane').classList.add('show', 'active');
  }

  else if (document.getElementById('productos-tab').classList.contains('active')) {
    document.getElementById('productos-tab').classList.remove('active');
    document.getElementById('pago-tab').classList.add('active');
    document.getElementById('productos-tab-pane').classList.remove('show', 'active');
    document.getElementById('pago-tab-pane').classList.add('show', 'active');
  }

}

function agregar_venta_ant_pestana() {

  if (document.getElementById('productos-tab').classList.contains('active')) {
    document.getElementById('productos-tab').classList.remove('active');
    document.getElementById('datos-tab').classList.add('active');
    document.getElementById('productos-tab-pane').classList.remove('show', 'active');
    document.getElementById('datos-tab-pane').classList.add('show', 'active');
  }

  else if (document.getElementById('pago-tab').classList.contains('active')) {
    document.getElementById('pago-tab').classList.remove('active');
    document.getElementById('productos-tab').classList.add('active');
    document.getElementById('pago-tab-pane').classList.remove('show', 'active');
    document.getElementById('productos-tab-pane').classList.add('show', 'active');
  }

}