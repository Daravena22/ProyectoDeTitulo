from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from app.modelos.abono import Abono
from app.modelos.tipo_abono import Tipo_abono
from sqlalchemy import or_ , func

api_pagos = Blueprint('api_pagos', __name__, url_prefix='/api/pagos')


@api_pagos.route("/agregar", methods=["PUT"])
@login_required
def agregar_pago():
    valores = request.get_json()
    cliente_id = valores['cliente']
    monto = int(valores['monto'])
    fecha = valores['fecha']
    tipo_abono = valores['tipo_abono']

    if monto > 0:
        abono = Abono()
        abono.monto = monto
        abono.cliente_id = cliente_id
        abono.fecha = fecha
        abono.tipo_abono_id = tipo_abono
        db.session.add(abono)

        # Actualizar la deuda del cliente
        cliente = db.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        cliente.deuda = cliente.deuda - monto

    db.session.commit()
    return jsonify({"status": 'ok'}), 200

@api_pagos.route("/listar", methods=["GET"])
@login_required
def listar_pagos():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start/pagina_lenght+1)
    draw = int(request.args.get("draw"))
    cliente = request.args.get('cliente')
    query = db.session.query(Abono.id,func.concat(Cliente.nombre, ' ', Cliente.apellido).label('cliente'),Abono.monto, Abono.fecha).join(Cliente, Abono.cliente_id == Cliente.id).filter(or_(Abono.cliente_id == cliente, cliente == '')).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})


from flask import abort

@api_pagos.route("/eliminar/<int:pago_id>", methods=["DELETE"])
@login_required
def eliminar_pago(pago_id):
 
    abono = db.session.query(Abono).filter(Abono.id == pago_id).first()

    if abono:
     
        cliente = db.session.query(Cliente).filter(Cliente.id == abono.cliente_id).first()
        cliente.deuda = cliente.deuda + abono.monto     
        db.session.delete(abono)
        db.session.commit()

        return jsonify({"status": 'ok'}), 200
    else:
        
        abort(404)
