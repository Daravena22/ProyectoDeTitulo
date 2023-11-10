from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.modelos.folios import Folios 
from app.modelos.producto import Producto
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from app.modelos.cliente import Cliente

api_ventas = Blueprint('api_ventas', __name__, url_prefix='/api/ventas')


@api_ventas.route("/agregar", methods=["PUT"])
@login_required
def agregar_venta():
    valores = request.get_json()
    lugar = valores['lugar']
    fecha = valores['fecha']
    cliente_id = valores['cliente']
    carrito = valores['carrito']
    folio = db.session.query(Folios).order_by(Folios.fecha_asignacion).first()


    return jsonify({"status":'ok'}), 200

    venta = Venta()
    venta.id = id
    venta.lugar = lugar
    venta.fecha = fecha
    venta.cliente_id = cliente_id
    

    db.session.add(venta)
    db.session.commit()
    return jsonify({"status":'ok'}), 200

@api_ventas.route("/listar", methods=["GET"])
@login_required
def listar_ventas():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start/pagina_lenght+1)
    draw = int(request.args.get("draw"))
    query = db.session.query(Venta.id ,Venta.fecha,Venta.folio, Venta.monto_bruto.label('total'),Venta.total_abonado.label('abonado')).join(Cliente,Venta.cliente_id == Cliente.id).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})
