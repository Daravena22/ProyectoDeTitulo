import pytest
from app import app
from app.modelos.producto import Producto

@pytest.fixture
def client():

    app.config["TESTING"] = True
    app.config["LOGIN_DISABLED"] = True
    with app.test_client() as client:
        yield client

def test_listar_productos(client):
    response = client.get('/api_productos/listar?length=10&start=0&draw=1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'recordsTotal' in data
    assert 'draw' in data
    assert 'recordsFiltered' in data

def test_datos_productos(client):
    
    producto_ejemplo = Producto(genero='Ejemplo', nombre='Producto de prueba', detalle='Detalles', precio=5000, stock=1, categoria_id=1, material_id=1)
    response = client.get(f'/api_productos/datosProductos/{producto_ejemplo.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'genero' in data
    assert 'nombre' in data
    assert 'detalle' in data
    assert 'precio' in data
    assert 'stock' in data
    assert 'categoria' in data
    assert 'material' in data



def test_listar_Producto(client):

    respuesta = client.get('/api/mantenedores/material/listartodo')
    assert respuesta.status_code == 200


def test_datos_productos(client):
      datos_cliente = {
          "rut": "12345678-9",
          "apellido": "Prueba",
          "nombre": "Unitaria",
          "telefono": "9652351",
          "direccion": "Calle"
     }
     
      respuesta = client.put('/api/clientes/agregar', json=datos_cliente)
      assert respuesta.status_code == 200


