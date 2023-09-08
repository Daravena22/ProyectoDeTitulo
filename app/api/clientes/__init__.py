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
    query = db.session.query(Cliente.id,Cliente.rut,Cliente.apellido,Cliente.nombre,Cliente.telefono,Cliente.direccion).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":1,"recordsFiltered":query.total})


