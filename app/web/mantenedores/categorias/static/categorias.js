const agregarCategoria = async () => {
    nombre = document.getElementById('nombreCategoria').value;
  
    const response = await fetch('/api/mantenedores/categorias/agregar', {
      method: 'PUT',
      body: JSON.stringify({ nombre: nombre }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    const myJson = await response.json();
    $('#nombreCategoria').val('');
    $('#datos_categorias').DataTable().ajax.reload();
    $('#AgregarCategoriaModal').modal('toggle');
  }
  
  $(document).ready(function () {
    $('#datos_categorias').DataTable({
      "processing": true,
      serverSide: true,
      ajax: {
        url: '/api/mantenedores/categorias/listar',
        type: 'GET',
      },
      columns: [
        { data: 'id', title: 'ID' },
        { data: 'nombre', title: 'Nombre' },
        {
          data: null, title: "ACCIONES",
          render: function (data, type, row) {
            return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarCategoria(' + row.id + ')">Eliminar</button>' +
              '<button type="button" class="btn btn-primary editar-btn" onclick="editarCategoria(' + row.id + ')">Editar</button>';
          }
        }
      ],
      "language": {
        "lengthMenu": "Mostrar _MENU_ registros por página",
        "zeroRecords": "No se han encontrado Categorías",
        "info": "Mostrando página _PAGE_ de _PAGES_",
        "search": "Buscar Categoría",
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
  
  const eliminarCategoria = async (id_categoria) => {
    const response = await fetch('/api/mantenedores/categorias/eliminar', {
      method: 'DELETE',
      body: JSON.stringify({ id: id_categoria }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    if(data.status == 'ok'){
      toastr.success('Categoria eliminada exitosamente')
      $('#datos_categorias').DataTable().ajax.reload();
    }
    else if (data.status == 'error'){
      toastr.error(data.message)
    }
    
    //extract JSON from the http response
    // do something with myJson
  }
  
  const editarCategoria = async (id_categoria) => {
    const response = await fetch(`/api/mantenedores/categorias/datosCategoria/` + id_categoria, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    const rowData = await response.json();
    $('#editar_id_categoria').val(id_categoria);
    $('#editar_nombre_categoria').val(rowData.nombre);
  
    $('#EditarCategoriaModal').modal('toggle');
  };
  
  const guardarEdicionCategoria = async () => {
    id_categoria = document.getElementById('editar_id_categoria').value;
    nombre = document.getElementById('editar_nombre_categoria').value;
  
    const response = await fetch('/api/mantenedores/categorias/editar', {
      method: 'PATCH',
      body: JSON.stringify({ id_categoria: id_categoria, nombre: nombre }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    const myJson = await response.json();
    $('#datos_categorias').DataTable().ajax.reload();
    $('#EditarCategoriaModal').modal('toggle');
    toastr.success('Categoría guardada exitosamente');
  }
  