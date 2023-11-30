from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.modelos.folios import Folios 
from app.modelos.producto import Producto
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from app.modelos.cliente import Cliente
from sqlalchemy import or_ , func, and_
from app.modelos.detalle_venta import Detalle_venta
from app.modelos.abono import Abono
from app.modelos.tipo_abono import Tipo_abono
from app.modelos.producto import Producto
from app.modelos.abono import Abono

api_ventas = Blueprint('api_ventas', __name__, url_prefix='/api/ventas')

VALOR_IVA = 0.19

@api_ventas.route("/agregar", methods=["PUT"])
@login_required
def agregar_venta():
    valores = request.get_json()
    lugar = valores['lugar']
    fecha = valores['fecha']
    cliente_id = valores['cliente']
    carrito = valores['carrito']
    abonado = int(valores['abonado'])
    tipo_abono = valores['tipo_abono']
    folios : Folios = db.session.query(Folios).filter(or_(Folios.ultimo_utilizado != Folios.rango_hasta,Folios.ultimo_utilizado == None)).order_by(Folios.fecha_asignacion).first()
    if folios.ultimo_utilizado is None:
        folio = folios.rango_desde
    else:
        folio = int(folios.ultimo_utilizado) + 1


    venta = Venta()
    venta.folio = folio
    venta.lugar = lugar
    venta.fecha = fecha
    venta.cliente_id = cliente_id
    venta.total_abonado = abonado
    
    monto_neto = 0.0
    
    for producto_id in carrito: 
        producto = carrito[producto_id]
        unidades = int(producto['cantidad'])
        precio = float(producto['precio'])
        monto_neto += precio*unidades
        producto = db.session.query(Producto).filter(Producto.id == producto_id).first()
        producto.stock = producto.stock - unidades
    

    venta.monto_neto = monto_neto
    impuesto = monto_neto*VALOR_IVA
    venta.monto_impuesto = impuesto
    venta.monto_bruto = monto_neto + impuesto
    db.session.add(venta)
    db.session.flush()

    for producto_id in carrito: 
        producto = carrito[producto_id]
        detalle_venta = Detalle_venta()
        detalle_venta.venta_id = venta.id
        detalle_venta.producto_id = producto_id
        detalle_venta.unidades = int(producto['cantidad'])
        db.session.add(detalle_venta)

    folios.ultimo_utilizado = folio
    
    if  abonado>0:
        abono = Abono()
        abono.monto = abonado
        abono.cliente_id = cliente_id
        abono.fecha = fecha
        abono.tipo_abono_id = tipo_abono
        db.session.add(abono)
        
    if venta.monto_bruto != abonado:

        cliente:Cliente = db.session.query(Cliente).filter(Cliente.id==cliente_id).first()
        monto = venta.monto_bruto - abonado
        cliente.deuda = cliente.deuda + monto

    db.session.commit()
    return jsonify({"status":'ok'}), 200

@api_ventas.route("/listar", methods=["GET"])
@login_required
def listar_ventas():
    pagina_lenght = int(request.args.get("length"))
    start = int(request.args.get("start"))
    pagina_index = int(start/pagina_lenght+1)
    draw = int(request.args.get("draw"))
    buscar = request.args.get("search[value]")
    buscar_or = [
        Cliente.rut.like(f"%{buscar}%"),
        Cliente.nombre.like(f"%{buscar}%"),
        Cliente.apellido.like(f"%{buscar}%"),
        Venta.folio.like(f"%{buscar}%")
    ]
    query = db.session.query(Venta.id ,Venta.fecha,Venta.folio,func.concat(Cliente.nombre, ' ', Cliente.apellido).label('cliente'), Venta.monto_bruto.label('total'),Venta.total_abonado.label('abonado')).join(Cliente,Venta.cliente_id == Cliente.id).filter(and_(or_(*buscar_or)), Cliente.estado==1, Venta.estado==1).paginate(page=pagina_index,per_page=pagina_lenght,error_out=False)
    rows=query.items
    data=SqlUtils.rows_to_dict(rows)
    return jsonify({"data": data, "recordsTotal": query.total,"draw":draw,"recordsFiltered":query.total})
