const agregarMaterial = async () => {

    nombre = document.getElementById('nombre').value

    const response = await fetch('/api/mantenedores/material/agregar', {
      method: 'PUT',
      body: JSON.stringify({nombre: nombre}), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json();
    $('#nombre').val('')
    $('#datos_material').DataTable().ajax.reload();
    $('#AgregarMaterialModal').modal('toggle')
    //extract JSON from the http response
    // do something with myJson
    
  }
  
  $(document).ready(function () {
    $('#datos_material').DataTable({
      "processing": true,
      serverSide: true,
      ajax: {
        url: '/api/mantenedores/material/listar',
        type: 'GET',
  
      },
      columns: [
        { data: 'id', title: 'ID' },
        { data: 'nombre', title: 'NOMBRE' },
      
        {
          data: null, title: "ACCIONES",
          render: function (data, type, row) {
            return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarMaterial(' + row.id + ')">Eliminar</button>' +
              '<button type="button" class="btn btn-primary editar-btn" onclick="editarMaterial(' + row.id + ')">Editar</button>';
          }
        }
  
        // Configura tus columnas aquí
      ]
    });
  });
  
  
  const eliminarMaterial = async (id_material) => {
    const response = await fetch('/api/mantenedores/material/eliminar', {
      method: 'DELETE',
      body: JSON.stringify({ id: id_material }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json();
    $('#datos_material').DataTable().ajax.reload();
    //extract JSON from the http response
    // do something with myJson
  }
  
  
  const editarMaterial = async (id_material) => {
    const response = await fetch(`/api/mantenedores/material/datosMaterial/` + id_material, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    const rowData = await response.json();
    $('#editar_id').val(id_material);
    $('#editar_nombre').val(rowData.nombre);
    
  
    $('#EditarMaterialModal').modal('toggle');
  };
  
  const guardarEdicion = async () => {
  
    id_material = document.getElementById('editar_id').value
    nombre = document.getElementById('editar_nombre').value

  
    const response = await fetch('/api/mantenedores/material/editar', {
      method: 'PATCH',
      body: JSON.stringify({ id_material: id_material, nombre: nombre}), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json();
    $('#datos_material').DataTable().ajax.reload();
    $('#EditarMaterialModal').modal('toggle')
    toastr.success('Material guardado exitosamente')
    //extract JSON from the http response
    // do something with myJson
  }