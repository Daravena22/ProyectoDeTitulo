from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.modelos.abono import Abono
from app.modelos.tipo_abono import Tipo_abono  
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from sqlalchemy import or_ , func, and_
import fpdf
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
from app.api.reportes.common import create_letterhead, create_title, write_to_pdf, PDF
from fpdf.fonts import FontFace
import os


api_reportePagos = Blueprint('api_reportePagos', __name__, url_prefix='/api/reportes/reportePagos')

@api_reportePagos.route("/generar", methods=["GET"])
@login_required
def generar_reporte():

    os.makedirs('tmp', exist_ok=True)

    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    rows = db.session.query(Abono.id, Cliente.rut,Cliente.apellido,Cliente.nombre,Abono.fecha, Abono.monto, Tipo_abono.nombre.label('tipo_abono')).join(Cliente, Abono.cliente_id == Cliente.id).join(Tipo_abono,Abono.tipo_abono_id==Tipo_abono.id).filter(and_(Abono.fecha>=fecha_desde,Abono.fecha<= fecha_hasta)).order_by(Abono.fecha).all()
    


    TITLE = "Reporte de Pagos"
    WIDTH = 210
    HEIGHT = 297

    # Create PDF
    pdf = PDF() # A4 (210 by 297 mm)


    '''
    First Page of PDF
    '''
    # Add Page
    pdf.add_page()

    # Add lettterhead and title
    create_letterhead(pdf, WIDTH)
    create_title(TITLE, pdf)

    # Add some words to PDF
    write_to_pdf(pdf, "Tabla con todos los pagos que se han realizado:")
    pdf.ln(15)

    # Add table
    # pdf.image("tmp/reporte_pagos.png", w=170)
    # pdf.ln(10)
    total = 0
    total_transferencia = 0
    total_efectivo = 0
    estilo_cabecera = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(57, 47, 90))
    estilo_monto = FontFace(emphasis="BOLD", color=(0, 100, 0))
    with pdf.table(borders_layout="MINIMAL",
               cell_fill_color=200,  # grey
               cell_fill_mode="ROWS",
               line_height=pdf.font_size * 2.5,
               text_align="CENTER",
               width=190,
               headings_style=estilo_cabecera) as table:
        row = table.row()
        row.cell('Rut')
        row.cell('Apellido')
        row.cell('Nombre')
        row.cell('Fecha')
        row.cell('Monto')
        row.cell('Tipo de Pago')
        for data_row in rows:
            row = table.row()
            for col,valor in enumerate(data_row):
                if col == 0: continue
                if col == 5:
                    row.cell(str(valor),style=estilo_monto)
                    total += valor 
                    if data_row.tipo_abono == 'Efectivo':
                        total_efectivo += valor
                    elif data_row.tipo_abono == 'Transferencia':
                        total_transferencia += valor
                else:
                    row.cell(str(valor))

    pdf.ln(15)
    write_to_pdf(pdf, "Total de montos Pagados: "+ str(total))
    pdf.ln(5)
    write_to_pdf(pdf, "Total de montos Pagados con Efectivo: "+ str(total_efectivo))
    pdf.ln(5)
    write_to_pdf(pdf, "Total de montos Pagados con Transferencia: "+ str(total_transferencia))

    pdf.output("tmp/reporte_pagos.pdf", 'F')

    return send_file('../tmp/reporte_pagos.pdf', mimetype='application/pdf')
