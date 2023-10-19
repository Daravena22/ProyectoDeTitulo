  const agregarProducto = async () => {
    response = await fetch(`/api/mantenedores/categorias/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    rowData = await response.json();
    const listadocategoria = document.getElementById('categoria');
    listadocategoria.innerHTML = "";
    rowData.data.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre;
      listadocategoria.appendChild(option);
    });

    
    response = await fetch(`/api/mantenedores/material/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    rowData = await response.json();
    const listadomaterial = document.getElementById('material');
    listadomaterial.innerHTML = "";
    rowData.data.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre;
      listadomaterial.appendChild(option);
    });

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

    if (/\d/.test(genero)) {
      mostrarMensajeError('El Genero no puede contener números.');
      return;
    }

    if (/\d/.test(nombre)) {
      mostrarMensajeError('El nombre no puede contener números.');
      return;
    }

    if (/[a-zA-Z]/.test(precio)) {
      mostrarMensajeError('El precio no puede contener letras.');
      return;
    }

    if (/[a-zA-Z]/.test(stock)) {
      mostrarMensajeError('El stock no puede contener letras.');
      return;
    }

    function mostrarMensajeError(mensaje) {
      // Utilizar Toastr.js u otra biblioteca similar para mostrar mensajes de error
      toastr.error(mensaje, 'Error', { timeOut: 3000 });
    }
  
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
    $('#AgregarProductoModal').modal('toggle')
    toastr.success('Producto guardado exitosamente')
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


  
  
  const eliminarProducto = async (id_producto) => {
    const response = await fetch('/api/productos/eliminar', {
      method: 'DELETE',
      body: JSON.stringify({ id: id_producto }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    if(data.status == 'ok'){
      toastr.success('Producto eliminado exitosamente')
      $('#datos_productos').DataTable().ajax.reload();
    }
    else if (data.status == 'error'){
      toastr.error(data.message)
    }}
  
  
  const editarProducto = async (id_producto) => {
    
    
    response = await fetch(`/api/mantenedores/categorias/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  
    rowData = await response.json();
    const listadocategoria = document.getElementById('editar_categoria');
    listadocategoria.innerHTML = "";
    rowData.data.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre;
      listadocategoria.appendChild(option);
    });

    
    response = await fetch(`/api/mantenedores/material/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    rowData = await response.json();
    const listadomaterial = document.getElementById('editar_material');
    listadomaterial.innerHTML = "";
    rowData.data.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre;
      listadomaterial.appendChild(option);
    });

    response = await fetch(`/api/productos/datosProductos/` + id_producto, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    rowData = await response.json();
    $('#editar_id_producto').val(id_producto);
    $('#editar_genero').val(rowData.genero);
    $('#editar_nombre').val(rowData.nombre);
    $('#editar_detalle').val(rowData.detalle);
    $('#editar_precio').val(rowData.precio);
    $('#editar_stock').val(rowData.stock);
    $('#editar_categoria').val(rowData.categoria);
    $('#editar_material').val(rowData.material);
  
    $('#EditarProductoModal').modal('toggle');
  };
  
  const guardarEdicion = async () => {

    id_producto = document.getElementById('editar_id_producto').value;
    genero = document.getElementById('editar_genero').value
    nombre = document.getElementById('editar_nombre').value
    detalle = document.getElementById('editar_detalle').value
    precio = document.getElementById('editar_precio').value
    stock = document.getElementById('editar_stock').value
    categoria = document.getElementById('editar_categoria').value
    material = document.getElementById('editar_material').value
  
    const response = await fetch('/api/productos/editar', {
      method: 'PATCH',
      body: JSON.stringify({id_producto : id_producto, genero: genero, nombre: nombre, detalle:detalle, precio: precio, stock: stock, categoria: categoria, material:material }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const myJson = await response.json();
    $('#datos_productos').DataTable().ajax.reload();
    $('#EditarProductoModal').modal('toggle')
    toastr.success('Producto guardado exitosamente')

    
    //extract JSON from the http response
    // do something with myJson
  }