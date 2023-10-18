const agregarProducto = async () => {
    response = await fetch(`/api/ventas/listartodo`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })};


    const agregarVentaGuardar = async () => {

        id = document.getElementById('id').value
        lugar = document.getElementById('lugar').value
        fecha = document.getElementById('detalle').value
        cliente= document.getElementById('cliente').value
        folios = document.getElementById('folios').value
       
        const response = await fetch('/api/ventas/agregar', {
          method: 'PUT',
          body: JSON.stringify({ id: id, lugar: lugar, fehca: fecha, cliente: cliente, folios: folios}), // string or object
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const myJson = await response.json();
        $('#id').val('')
        $('#lugar').val('')
        $('#fecha').val('')
        $('#cliente').val(0)
        $('#folios').val(0)
    
        $('#datos_ventas').DataTable().ajax.reload();
        $('#AgregarVentasModal').modal('toggle')
        //extract JSON from the http response
        // do something with myJson
        
      }
      
      $(document).ready(function () {
        $('#datos_ventas').DataTable({
          "processing": true,
          serverSide: true,
          ajax: {
            url: '/api/ventas/listar',
            type: 'GET',
      
          },
          columns: [
            
            { data: 'id', title: 'ID' },
            { data: 'lugar', title: 'LUGAR' },
            { data: 'fecha', title: 'FECHA' },
            { data: 'cliente', title: 'CLIENTE' },
            { data: 'folios', title: 'FOLIOS' },
            
            {
              data: null, title: "ACCIONES",
              render: function (data, type, row) {
                return '<button type="button" class="btn btn-danger eliminar-btn" onclick="eliminarVenta(' + row.id + ')">Eliminar</button>' +
                  '<button type="button" class="btn btn-primary editar-btn" onclick="editarVenta(' + row.id + ')">Editar</button>';
              }
            }
      
            // Configura tus columnas aquí
          ]
        });
      });
    

      const eliminarVenta = async (id_venta) => {
        const response = await fetch('/api/ventas/eliminar', {
          method: 'DELETE',
          body: JSON.stringify({ id: id_venta }), // string or object
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        if(data.status == 'ok'){
          toastr.success('Venta eliminada exitosamente')
          $('#datos_ventas').DataTable().ajax.reload();
        }
        else if (data.status == 'error'){
          toastr.error(data.message)
        }}
            