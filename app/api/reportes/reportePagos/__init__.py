from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.modelos.abono import Abono
from app.modelos.tipo_abono import Tipo_abono  
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from sqlalchemy import or_ , func
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

    rows = db.session.query(Abono.id, Cliente.rut,Cliente.apellido,Cliente.nombre,Abono.fecha, Abono.monto, Tipo_abono.nombre).join(Cliente, Abono.cliente_id == Cliente.id).join(Tipo_abono,Abono.tipo_abono_id==Tipo_abono.id).all()
    

    # def color_pos_neg_value(value):
    #     if value > 0:
    #         color = 'green'
    #     elif value < 0:
    #         color = 'red'
    #     else:
    #         color = 'black'
    #     return 'color: %s' % color
     
    # df.rename(columns={'rut':'RUT', 'apellido':'Apellido', 'nombre':'Nombre', 'monto': 'Monto', 'fecha':'Fecha'}, inplace=True)
    # styled_df = df.style.format({ 
    #     'Monto': "{:.0f}",
    #     }).hide(axis='index').applymap(color_pos_neg_value, subset=['Monto'])
    
    # dfi.export(styled_df, 'tmp/reporte_pagos.png')

    # Global Variables
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
                else:
                    row.cell(str(valor))

    pdf.ln(15)
    write_to_pdf(pdf, "Total de montos Pagados: "+ str(total))

    pdf.output("tmp/reporte_pagos.pdf", 'F')

    return send_file('../tmp/reporte_pagos.pdf', mimetype='application/pdf')
