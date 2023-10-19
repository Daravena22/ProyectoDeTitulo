import pytest
from flask import Flask, json
from app import app
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from app.api.clientes import api_clientes
from app.api.clientes import agregar_cliente
from app.modelos.cliente import Cliente


def test_agregar_cliente():
   
    datos_cliente = {
        'rut': '19726548-5',
        'apellido': 'Aravena',
        'nombre': 'Daniel',
        'telefono': '123456789',
        'direccion': 'Calle 123'
    }

  
    response, status_code = agregar_cliente(json.dumps(datos_cliente))
    api_clientes.agregar_cliente()

    assert status_code == 200
    assert response['status'] == 'ok'