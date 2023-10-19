const agregarFolios = async () => {

    const archivo = document.getElementById("archivo");
    const file = archivo.files[0];

    const formData = new FormData();
        formData.append("file", file);

 
    const response = await fetch('/api/mantenedores/folios/agregar', {
        method: 'PUT',
        body: formData, // string or object
        // headers: {
        //     'Content-Type': 'application/json'
        // }
    });
    const myJson = await response.json();

    $('#datos_folios').DataTable().ajax.reload();
    $('#CargarFoliosModal').modal('toggle')
    toastr.success('Folios cargados exitosamente')
    //extract JSON from the http response
    // do something with myJson

}

$(document).ready(function () {
    $('#datos_folios').DataTable({
        "processing": true,
        serverSide: true,
        ajax: {
            url: '/api/mantenedores/folios/listar',
            type: 'GET',

        },
        columns: [
            { data: 'fecha_asignacion', title: 'FECHA ASIGNACION' },
            { data: 'fecha_vencimiento', title: 'FECHA VENCIMIENTO' },
            { data: 'rango_desde', title: 'RANGO DESDE' },
            { data: 'rango_hasta', title: 'RANGO HASTA' },
            { data: 'ultimo_utilizado', title: 'ULTIMO UTILIZADO' },
           
            {
                data: null, title: "ACCIONES",
                render: function (data, type, row) {
                    return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarFolios(' + row.id + ')">Eliminar</button>'; 
                        
                }
            }

            // Configura tus columnas aquí
        ]
    });
});

const eliminarFolios = async (id_folios) => {
    const response = await fetch('/api/mantenedores/folios/eliminar', {
      method: 'DELETE',
      body: JSON.stringify({ id: id_folios }), // string or object
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    if(data.status == 'ok'){
      toastr.success('Folios eliminados exitosamente')
      $('#datos_folios').DataTable().ajax.reload();
    }
    else if (data.status == 'error'){
      toastr.error(data.message)
    }
    
    //extract JSON from the http response
    // do something with myJson
  }