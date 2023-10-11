  const agregarProducto = async () => {
    const response = await fetch(`/api/mantenedores/categorias/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    const rowData = await response.json();
    //$('#editar_id').val(id_cliente);
    $('#AgregarProductoModal').modal('toggle');
  };

const agregarProductoGuardar = async () => {

    genero = document.getElementById('genero').value
    nombre = document.getElementById('nombre').value
    detalle = document.getElementById('detalle').value
    precio= document.getElementById('precio').value
    stock = document.getElementById('stock').value
    categoria = document.getElementById('categoria').value
    material = document.getElementById('material').value
  
    const response = await fetch('/api/productos/agregar', {
      method: 'PUT',
      body: JSON.stringify({ genero: genero, nombre: nombre, detalle: detalle, precio: precio, stock: stock, categoria: categoria, material: material }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json();
    $('#genero').val('')
    $('#nombre').val('')
    $('#detalle').val('')
    $('#precio').val(0)
    $('#stock').val(0)
    $('#categoria').val('')
    $('#material').val('')

    $('#datos_productos').DataTable().ajax.reload();
    $('#AgregarProductosModal').modal('toggle')
    //extract JSON from the http response
    // do something with myJson
    
  }
  
  $(document).ready(function () {
    $('#datos_productos').DataTable({
      "processing": true,
      serverSide: true,
      ajax: {
        url: '/api/productos/listar',
        type: 'GET',
  
      },
      columns: [
        { data: 'genero', title: 'GENERO' },
        { data: 'nombre', title: 'NOMBRE' },
        { data: 'detalle', title: 'DETALLE' },
        { data: 'precio', title: 'PRECIO' },
        { data: 'stock', title: 'STOCK' },
        { data: 'categoria', title: 'CATEGORIA' },
        { data: 'material', title: 'MATERIAL' },
        {
          data: null, title: "ACCIONES",
          render: function (data, type, row) {
            return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarProducto(' + row.id + ')">Eliminar</button>' +
              '<button type="button" class="btn btn-primary editar-btn" onclick="editarProducto(' + row.id + ')">Editar</button>';
          }
        }
  
        // Configura tus columnas aquí
      ]
    });
  });


  
  
//   const eliminarCliente = async (id_cliente) => {
//     const response = await fetch('/api/clientes/eliminar', {
//       method: 'DELETE',
//       body: JSON.stringify({ id: id_cliente }), // string or object
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     });
//     const myJson = await response.json();
//     $('#datos_clientes').DataTable().ajax.reload();
//     //extract JSON from the http response
//     // do something with myJson
//   }
  
  
//   const editarCliente = async (id_cliente) => {
//     const response = await fetch(`/api/clientes/datosCliente/` + id_cliente, {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     });
  
//     const rowData = await response.json();
//     $('#editar_id').val(id_cliente);
//     $('#editar_rut').val(rowData.rut);
//     $('#editar_apellido').val(rowData.apellido);
//     $('#editar_nombre').val(rowData.nombre);
//     $('#editar_telefono').val(rowData.telefono);
//     $('#editar_direccion').val(rowData.direccion);
  
//     $('#EditarClienteModal').modal('toggle');
//   };
  
//   const guardarEdicion = async () => {
  
//     id_cliente = document.getElementById('editar_id').value
//     rut = document.getElementById('editar_rut').value
//     apellido = document.getElementById('editar_apellido').value
//     nombre = document.getElementById('editar_nombre').value
//     telefono = document.getElementById('editar_telefono').value
//     direccion = document.getElementById('editar_direccion').value
  
//     const response = await fetch('/api/clientes/editar', {
//       method: 'PATCH',
//       body: JSON.stringify({ id_cliente: id_cliente, rut: rut, apellido: apellido, nombre: nombre, telefono: telefono, direccion: direccion }), // string or object
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     });
//     const myJson = await response.json();
//     $('#datos_clientes').DataTable().ajax.reload();
//     $('#EditarClienteModal').modal('toggle')
//     toastr.success('Cliente guardado exitosamente')
//     //extract JSON from the http response
//     // do something with myJson
//   }