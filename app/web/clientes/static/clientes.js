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

