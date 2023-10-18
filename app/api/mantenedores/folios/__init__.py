from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.common.sql_utils import SqlUtils
from app.modelos.folios import Folios
import xmltodict 


api_folios = Blueprint('api_folios', __name__, url_prefix='/api/mantenedores/folios')

@api_folios.route("/agregar", methods=["PUT"])
@login_required
def agregar_folios():
    archivo = request.files['file']
    contenido = archivo.read()
    contenido = xmltodict.parse(contenido)
    fecha_asignacion = contenido ["AUTORIZACION"]["CAF"]["DA"]["FA"]
    rango_desde = contenido ["AUTORIZACION"]["CAF"]["DA"]["RNG"]["D"]
    rango_hasta = contenido ["AUTORIZACION"]["CAF"]["DA"]["RNG"]["H"]
    rsapk = contenido ["AUTORIZACION"]["CAF"]["DA"]["RSAPK"]["M"]
    frma = contenido ["AUTORIZACION"]["CAF"]["FRMA"]["#text"]
    rsask = contenido ["AUTORIZACION"]["RSASK"]
    rsapubk = contenido ["AUTORIZACION"]["RSAPUBK"]

    folios = Folios()
    folios.fecha_asignacion = fecha_asignacion
    folios.rango_desde = rango_desde
    folios.rango_hasta = rango_hasta
    folios.rsapk = rsapk
    folios.frma = frma
    folios.rsask = rsask
    folios.rsapubk = rsapubk

    db.session.add(folios)
    db.session.commit()

    return jsonify({"status":'ok'}), 200

@api_folios.route("/listar", methods=["GET"])
@login_required
def listar_folios():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start / pagina_lenght + 1)
    draw = int(request.args.get("draw"))
    
    query = db.session.query(Folios.id, Folios.fecha_asignacion, Folios.rango_desde, Folios.rango_hasta, Folios.ultimo_utilizado).paginate(page=pagina_index, per_page=pagina_lenght, error_out=False)
    rows = query.items
    data = SqlUtils.rows_to_dict(rows)
    for fila in data:
        fila["fecha_vencimiento"] = fila["fecha_asignacion"] + relativedelta(months = 6)
    
    return jsonify({"data": data, "recordsTotal": query.total, "draw": draw, "recordsFiltered": query.total})

@api_folios.route("/eliminar", methods=["DELETE"])
@login_required
def eliminar_folios():
    valores = request.get_json()
    id = valores["id"]
    folios = db.session.query(Folios).filter(Folios.id==id).first()
    db.session.delete(folios)
    db.session.commit()
    return jsonify({"status":'ok'}), 200
