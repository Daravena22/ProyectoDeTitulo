from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils

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


@api_clientes.route("/listar", methods=["GET"])
@login_required
def listar_clientes():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start/pagina_lenght+1)
    draw = int(request.args.get("draw"))
    query = db.session.query(Cliente.id,Cliente.rut,Cliente.apellido,Cliente.nombre,Cliente.telefono,Cliente.direccion).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})

@api_clientes.route("/eliminar", methods=["DELETE"])
@login_required
def eliminar_cliente():
    valores = request.get_json()
    id = valores["id"]
    cliente = db.session.query(Cliente).filter(Cliente.id==id).first()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"status":'ok'}), 200



@api_clientes.route("/datosCliente/<id_cliente>", methods=["GET"])
@login_required
def datos_cliente(id_cliente):

  
    # Obtén el cliente que deseas editar desde la base de datos
    cliente = db.session.query(Cliente).filter(Cliente.id == id_cliente).first()
    
    # Devuelve los datos del cliente como JSON, incluso si el cliente no se encuentra
    cliente_data = {
        "rut": cliente.rut,
        "apellido": cliente.apellido,
        "nombre": cliente.nombre,
        "telefono": cliente.telefono,
        "direccion": cliente.direccion
    }
    return jsonify(cliente_data), 200



@api_clientes.route("/editar", methods=["PATCH"])
@login_required
def editar_cliente():
    valores = request.get_json()
    
    id_cliente = valores["id_cliente"]
    rut = valores['rut']
    apellido = valores['apellido']
    nombre = valores['nombre']
    telefono = valores['telefono']
    direccion = valores['direccion']

    cliente = db.session.query(Cliente).filter(Cliente.id == id_cliente).first()
    cliente.rut = rut
    cliente.apellido = apellido
    cliente.nombre = nombre
    cliente.telefono = telefono
    cliente.direccion = direccion


    db.session.commit()
    return jsonify({"status":'ok'}), 200

    
   



