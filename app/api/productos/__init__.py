from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.producto import Producto
from app.modelos.material import Material
from app.modelos.categoria import Categoria 
from app.common.sql_utils import SqlUtils
from sqlalchemy import or_, and_

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
    query = db.session.query(Producto.id, Producto.genero ,Producto.nombre,Producto.detalle,Producto.precio,Producto.stock, Categoria.nombre.label('categoria'),Material.nombre.label('material')).join(Categoria,Producto.categoria_id == Categoria.id).join(Material, Producto.material_id == Material.id).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})


@api_productos.route("/datosProductos/<id_producto>", methods=["GET"])
@login_required
def datos_productos(id_producto):

    producto = db.session.query(Producto).filter(Producto.id == id_producto).first()

    producto_data = {
        
        "genero" : producto.genero,
        "nombre": producto.nombre,
        "detalle" : producto.detalle,
        "precio" : producto.precio,
        "stock" : producto.stock,
        "categoria" : producto.categoria_id,
        "material" : producto.material_id

    }
    return jsonify(producto_data), 200

@api_productos.route("/eliminar", methods=["DELETE"])
@login_required
def eliminar_producto():
    valores = request.get_json()
    id = valores["id"]
    producto = db.session.query(Producto).filter(Producto.id== id).first()

    db.session.delete(producto)
    db.session.commit()
    return jsonify({"status":'ok'}), 200

@api_productos.route("/listartodo", methods=["GET"])
@login_required
def listar_todos_productos():
    
    rows = db.session.query(Producto.id,Producto.nombre,Producto.detalle, Producto.precio, Producto.stock).filter(Producto.stock>0).all()
    data = SqlUtils.rows_to_dict(rows)
    
    return jsonify({"data": data})

@api_productos.route("/editar", methods=["PATCH"])
@login_required
def editar_producto():
    valores = request.get_json()
    
    id_producto = valores["id_producto"]
    genero = valores['genero']
    nombre = valores['nombre']
    detalle = valores['detalle']
    precio = valores['precio']
    stock = valores['stock']
    categoria = valores['categoria']
    material = valores['material']

    producto = db.session.query(Producto).filter(Producto.id == id_producto).first()
    producto.genero = genero
    producto.nombre = nombre
    producto.detalle = detalle
    producto.precio = precio
    producto.categoria_id = categoria
    producto.material_id = material


    db.session.commit()
    return jsonify({"status":'ok'}), 200


