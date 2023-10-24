const agregarVenta = async () => {
  response = await fetch(`/api/clientes/listartodo`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  rowData = await response.json();
  const listadocliente = document.getElementById('clientes');
  listadocliente.innerHTML = "";
  rowData.data.forEach(item => {
    const option = document.createElement('option');
    option.setAttribute('data-value', item.id)
    option.value = item.nombre + ' ' + item.apellido + ' ' + item.rut;
    listadocliente.appendChild(option);
  });

  $('#AgregarVentaModal').modal('toggle');
};