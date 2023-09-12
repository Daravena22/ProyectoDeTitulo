const agregarCliente = async () => {
    
    rut = document.getElementById('rut').value
    apellido = document.getElementById('apellido').value
    nombre = document.getElementById('nombre').value
    telefono = document.getElementById('telefono').value
    direccion = document.getElementById('direccion').value
    
    const response = await fetch('/api/clientes/agregar', {
      method: 'PUT',
      body:JSON.stringify({rut:rut,apellido:apellido,nombre:nombre,telefono:telefono,direccion:direccion}), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json(); 
    $('#rut').val('')
    $('#datos_clientes').DataTable().ajax.reload();
    $('#AgregarClienteModal').modal('toggle')
    //extract JSON from the http response
    // do something with myJson
  }

  $(document).ready(function() {
    $('#datos_clientes').DataTable({
      "processing": true,
        serverSide: true,
        ajax: {
            url: '/api/clientes/listar',
            type: 'GET',
            
        },
        columns: [
          { data: 'id', title: 'ID' },
          { data: 'rut', title: 'RUT' },
          { data: 'apellido', title: 'APELLIDO' },
          { data: 'nombre', title: 'NOMBRE' },
          { data: 'telefono', title: 'TELEFONO' },
          { data: 'direccion', title: 'DIRECCION' },
          {
            data: null, title: "ACCIONES",
            render: function (data, type, row) {
              return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarCliente(' + row.id + ')">Eliminar</button>' +
                     '<button type="button" class="btn btn-primary editar-btn" onclick="editarCliente(' + row.id + ')">Editar</button>';
            }
          }
          
            // Configura tus columnas aquí
        ]
    });
});


const eliminarCliente = async (id_cliente) => { 
  const response = await fetch('/api/clientes/eliminar', {
    method: 'DELETE',
    body:JSON.stringify({id:id_cliente}), // string or object
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const myJson = await response.json(); 
  $('#datos_clientes').DataTable().ajax.reload();
  //extract JSON from the http response
  // do something with myJson
}

const editarCliente = async (id_cliente) => {
  // Recopila los datos del formulario de edición aquí
  const rut = document.getElementById('editar_rut').value;
  const apellido = document.getElementById('editar_apellido').value;
  const nombre = document.getElementById('editar_nombre').value;
  const telefono = document.getElementById('editar_telefono').value;
  const direccion = document.getElementById('editar_direccion').value;

  const data = {
    id: id_cliente,
    rut: rut,
    apellido: apellido,
    nombre: nombre,
    telefono: telefono,
    direccion: direccion
  };

  const response = await fetch('/api/clientes/editar', {
    method: 'UPDATE',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  const myJson = await response.json();
  $('#datos_clientes').DataTable().ajax.reload();
  // Extrae JSON de la respuesta HTTP
  // Haz algo con myJson si es necesario
}


