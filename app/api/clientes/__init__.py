from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.cliente import Cliente 

api_clientes = Blueprint('api_clientes', __name__, url_prefix='/api/clientes')


@api_clientes.route("/agregar", methods=["PUT"])
@login_required
def agregar_cliente():
    valores = request.get_json()
    rut= valores['rut']
    apellido = valores['apellido']
    nombre = valores['nombre']
    telefono = valores['telefono']
    direccion = valores['direccion']

    cliente = Cliente()
    cliente.rut = rut
    cliente.apellido = apellido
    cliente.nombre = nombre
    cliente.telefono = telefono
    cliente.direccion = direccion

    db.session.add(cliente)
    db.session.commit()
    return jsonify({"status":'ok'}), 200


    