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
          { data: 'direccion', title: 'DIRECCION' }
            // Configura tus columnas aquí
        ]
    });
});

