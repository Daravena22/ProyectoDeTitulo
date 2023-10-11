from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.producto import Producto
from app.modelos.material import Material
from app.modelos.categoria import Categoria 
from app.common.sql_utils import SqlUtils

api_productos = Blueprint('api_productos', __name__, url_prefix='/api/productos')


@api_productos.route("/agregar", methods=["PUT"])
@login_required
def agregar_productos():
    valores = request.get_json()
    genero = valores['genero']
    nombre = valores['nombre']
    detalle = valores['detalle']
    precio = valores['precio']
    stock = valores['stock']
    categoria_id = valores['categoria']
    material_id = valores['material']

    producto = Producto()
    producto.genero = genero
    producto.nombre = nombre
    producto.detalle = detalle
    producto.precio = precio
    producto.stock = stock
    producto.categoria_id = categoria_id
    producto.material_id = material_id 

    db.session.add(producto)
    db.session.commit()
    return jsonify({"status":'ok'}), 200


@api_productos.route("/listar", methods=["GET"])
@login_required
def listar_productos():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start/pagina_lenght+1)
    draw = int(request.args.get("draw"))
    query = db.session.query(Producto.id, Producto.genero ,Producto.nombre,Producto.detalle,Producto.precio,Producto.stock, Categoria.nombre.alias('dategoria'),Material.nombre.alias('material')).join(Categoria,Producto.categoria_id, Categoria.id).join(Material, Producto.material_id, Material.id).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})