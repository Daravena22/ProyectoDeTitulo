import pytest
from app import app

@pytest.fixture
def client():

    app.config["TESTING"] = True
    app.config["LOGIN_DISABLED"] = True
    with app.test_client() as client:
        yield client
           
# def test_listar_cliente(client):

#     respuesta = client.get('/api/mantenedores/material/listartodo')
#     assert respuesta.status_code == 200


# def test_agregar_cliente(client):
#       datos_cliente = {
#           "rut": "12345678-9",
#           "apellido": "Prueba",
#           "nombre": "Unitaria",
#           "telefono": "9652351",
#           "direccion": "Calle"
#      }
     
#       respuesta = client.put('/api/clientes/agregar', json=datos_cliente)
#       assert respuesta.status_code == 200



# def test_eliminar_cliente(client):
#     datos_eliminar = {"id": 41} 
#     respuesta = client.delete('/api/clientes/eliminar', json=datos_eliminar)
#     assert respuesta.status_code == 200