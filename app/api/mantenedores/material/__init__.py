from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.common.sql_utils import SqlUtils
from app.modelos.material import Material

api_material = Blueprint('api_material', __name__, url_prefix='/api/mantenedores/material')


@api_material.route("/agregar", methods=["PUT"])
@login_required
def agregar_material():
    valores = request.get_json()
    nombre = valores['nombre']

    material = Material()
    material.nombre = nombre

    db.session.add(material)
    db.session.commit()
    return jsonify({"status":'ok'}), 200


@api_material.route("/listar", methods=["GET"])
@login_required
def listar_material():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start/pagina_lenght+1)
    draw = int(request.args.get("draw"))
    query = db.session.query(Material.id,Material.nombre).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})

@api_material.route("/eliminar", methods=["DELETE"])
@login_required
def eliminar_material():
    valores = request.get_json()
    id = valores["id"]
    cliente = db.session.query(Material).filter(Material.id==id).first()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"status":'ok'}), 200



@api_material.route("/datosMaterial/<id_material>", methods=["GET"])
@login_required
def datos_material(id_material):

  
    # Obtén el cliente que deseas editar desde la base de datos
    material = db.session.query(Material).filter(Material.id == id_material).first()
    
    # Devuelve los datos del cliente como JSON, incluso si el cliente no se encuentra
    material_data = {
        
  
        "nombre": material.nombre

    }
    return jsonify(material_data), 200



@api_material.route("/editar", methods=["PATCH"])
@login_required
def editar_material():
    valores = request.get_json()
    
    id_material = valores["id_material"]
    nombre = valores['nombre']


    material = db.session.query(Material).filter(Material.id == id_material).first()
   
    material.nombre = nombre
    db.session.commit()
    return jsonify({"status":'ok'}), 200

@api_material.route("/listartodo", methods=["GET"])
@login_required
def listar_todos_material():
    
    rows = db.session.query(Material.id, Material.nombre).all()
    data = SqlUtils.rows_to_dict(rows)
    
    return jsonify({"data": data})
   



