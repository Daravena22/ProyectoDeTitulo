from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.modelos.categoria import Categoria  # Asegúrate de importar la clase de modelo correcta
from app.common.sql_utils import SqlUtils

api_categorias = Blueprint('api_categorias', __name__, url_prefix='/api/mantenedores/categorias')

@api_categorias.route("/agregar", methods=["PUT"])
@login_required
def agregar_categoria():
    valores = request.get_json()
    nombre = valores['nombre']  # Asegúrate de que coincida con el nombre del campo en el formulario

    categoria = Categoria()
    categoria.nombre = nombre

    db.session.add(categoria)
    db.session.commit()
    return jsonify({"status": 'ok'}), 200

@api_categorias.route("/listar", methods=["GET"])
@login_required
def listar_categorias():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start / pagina_lenght + 1)
    draw = int(request.args.get("draw"))
    
    query = db.session.query(Categoria.id, Categoria.nombre).paginate(page=pagina_index, per_page=pagina_lenght, error_out=False)
    rows = query.items
    data = SqlUtils.rows_to_dict(rows)
    
    return jsonify({"data": data, "recordsTotal": query.total, "draw": draw, "recordsFiltered": query.total})

@api_categorias.route("/eliminar", methods=["DELETE"])
@login_required
def eliminar_categoria():
    valores = request.get_json()
    id = valores["id"]
    categoria = db.session.query(Categoria).filter(Categoria.id == id).first()
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"status": 'ok'}), 200

@api_categorias.route("/datosCategoria/<id_categoria>", methods=["GET"])
@login_required
def datos_categorias(id_categoria):
    categoria = db.session.query(Categoria).filter(Categoria.id == id_categoria).first()
    
    categoria_data = {
        "nombre": categoria.nombre
    }
    
    return jsonify(categoria_data), 200

@api_categorias.route("/editar", methods=["PATCH"])
@login_required
def editar_categoria():
    valores = request.get_json()
    
    id_categoria = valores["id_categoria"]
    nombre = valores['nombre']
    
    categoria = db.session.query(Categoria).filter(Categoria.id == id_categoria).first()
    categoria.nombre = nombre

    db.session.commit()
    return jsonify({"status": 'ok'}), 200

@api_categorias.route("/listartodo", methods=["GET"])
@login_required
def listar_todos_categorias():
    
    rows = db.session.query(Categoria.id, Categoria.nombre).all()
    data = SqlUtils.rows_to_dict(rows)
    
    return jsonify({"data": data})