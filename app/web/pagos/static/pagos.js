clientes = {}

const agregarPago = async () => {
  response = await fetch(`/api/clientes/listartodo_deuda`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  clientes={}
  rowData = await response.json();
  const listadocliente = document.getElementById('pago_cliente');
  listadocliente.innerHTML = "";
  rowData.data.forEach(item => {
    const option = document.createElement('option');
    option.value = item.id;
    option.textContent = item.nombre + ' ' + item.apellido;
    listadocliente.appendChild(option);
    clientes[item.id] = item.deuda;
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
    
console.log(clientes)


seleccionar_cliente(document.getElementById('pago_cliente'))
$('#monto').val(0);
$('#AgregarPagoModal').modal('toggle');


}



function seleccionar_cliente(id_cliente) {
  id_cliente = id_cliente.value
  console.log(id_cliente)
  var deuda = clientes[id_cliente];
  console.log(deuda)
  $('#deuda').val(deuda);
}

const guardarPago = async () => {

  cliente = document.getElementById('pago_cliente').value
  monto = document.getElementById('monto').value
  fecha = document.getElementById('fecha').value
  tipo_abono = document.getElementById('tipo_abono').value

  const response = await fetch('/api/pagos/agregar', {
    method: 'PUT',
    body: JSON.stringify({cliente: cliente, monto:monto,fecha:fecha, tipo_abono:tipo_abono}), // string or object
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const myJson = await response.json();
  $('#pago_cliente').val('')
  $('#fecha').val('')

  $('#datos_pagos').DataTable().ajax.reload();
  $('#AgregarPagoModal').modal('toggle')
  toastr.success('Pago guardado exitosamente')
}

$(document).ready(function () {
  cargar_clientes()
  $('#datos_pagos').DataTable({
    "processing": true,
    serverSide: true,
    ajax: {
      url: '/api/pagos/listar',
      data:function(d){
        d.cliente = document.getElementById('cliente').value
      },
      type: 'GET',

    },
    columns: [

      { data: 'cliente', title: 'CLIENTE' },
      { data: 'monto', title: 'MONTO PAGADO' },
      { data: 'fecha', title: 'FECHA DE PAGO' },
      {
        data: null, title: "ACCIONES",
        render: function (data, type, row) {
          return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarPago(' + row.id + ')">Anular Pago</button>' 
            
        }
      }


    ],

    "language": {
      "lengthMenu": "Mostrar _MENU_ registros por página",
      "zeroRecords": "Cliente no registra Pago",
      "info": "Mostrando página _PAGE_ de _PAGES_",
      "search": "Buscar Pago",
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

const cargar_clientes = async (id_cliente) =>{
  response = await fetch(`/api/clientes/listartodo`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  rowData = await response.json();
  const listadocliente = document.getElementById('cliente');
  listadocliente.innerHTML = "";
  const option = document.createElement('option');
  option.value = '';
  option.textContent = 'Todos';
  listadocliente.appendChild(option);
  rowData.data.forEach(item => {
    const option = document.createElement('option');
    option.value = item.id;
    option.textContent = item.nombre + ' ' + item.apellido;
    listadocliente.appendChild(option);
  });
}

function cargar_datos_cliente(){

$('#datos_pagos').DataTable().ajax.reload();

}

const eliminarPago = (id_abono) => {

  $('#confirmarEliminarModal').modal('show');
  $('#confirmarEliminarBtn').on('click', async () => {
    const response = await fetch(`/api/pagos/eliminar/${id_abono}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const myJson = await response.json();
    $('#datos_pagos').DataTable().ajax.reload();
    $('#confirmarEliminarModal').modal('hide');

  });
};
