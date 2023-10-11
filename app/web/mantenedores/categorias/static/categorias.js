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
      ]
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
  
    const myJson = await response.json();
    $('#datos_categorias').DataTable().ajax.reload();
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
  