from datetime import datetime, timedelta
from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.modelos.abono import Abono 
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from sqlalchemy import and_, func
import fpdf
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
from app.api.reportes.common import create_letterhead, create_title, write_to_pdf, PDF
from fpdf.fonts import FontFace




api_reporteVentas = Blueprint('api_reporteVentas', __name__, url_prefix='/api/reportes/reporteVentas')

@api_reporteVentas.route("/generar", methods=["GET"])
@login_required
def generar_reporte():

    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    rows = db.session.query(Venta.id ,func.concat(Cliente.nombre, ' ', Cliente.apellido).label('cliente'),Venta.fecha,Venta.folio, Venta.monto_bruto.label('total'),Venta.total_abonado.label('abonado')).join(Cliente,Venta.cliente_id == Cliente.id).filter(and_(Venta.fecha>=fecha_desde,Venta.fecha<= fecha_hasta)).order_by(Venta.fecha)

    TITLE = "Reporte de Ventas"
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

    write_to_pdf(pdf, "Ventas generadas entre: "+ fecha_desde + " y " + fecha_hasta)
    pdf.ln(10)

    total_venta = 0
    total_pagado = 0
    estilo_cabecera = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(57, 47, 90))
    estilo_monto = FontFace(emphasis="BOLD", color=(0, 100, 0))
    estilo_total = FontFace(emphasis="BOLD", color=(0, 0, 100))
    with pdf.table(borders_layout="MINIMAL",
               cell_fill_color=200,  # grey
               cell_fill_mode="ROWS",
               line_height=pdf.font_size * 2.5,
               text_align="CENTER",
               width=190,
               headings_style=estilo_cabecera) as table:
        row = table.row()
        row.cell('Cliente')
        row.cell('Fecha')
        row.cell('Folio')
        row.cell('Total')
        row.cell('Abonado')
        for data_row in rows:
            row = table.row()
            for col,valor in enumerate(data_row):
                if col == 0: continue
                if col == 5:
                    row.cell(str(valor),style=estilo_monto)
                    total_pagado += valor
                elif col == 4:
                    row.cell(str(valor),style=estilo_total)
                    total_venta += valor
                else:
                    row.cell(str(valor))
    
    pdf.ln(10)
    write_to_pdf(pdf, "Total de Ventas: "+ str(total_venta))
    pdf.ln(10)
    write_to_pdf(pdf, "Total de montos Pagados: "+ str(total_pagado))

    datos = []
    fecha = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
    fecha = fecha - timedelta(days=fecha.weekday())
    pagado = 0
    monto = 0 

    for row in rows:
        if row.fecha > fecha + timedelta(days=6):
            datos.append((fecha,fecha + timedelta(days=6),monto,pagado))
            fecha=fecha + timedelta(days=7)
            pagado = 0
            monto = 0
        monto+=row.total
        pagado+=row.abonado
    datos.append((fecha,fecha + timedelta(days=6),monto,pagado))
    
    datos = pd.DataFrame(data=datos,  
               columns=['fecha_desde','fecha_hasta','total', 'pagado'])



    pdf.add_page() 
    pdf.ln(5) 
    write_to_pdf(pdf, "Grafica comparativa entre montos de Ventas y montos Pagados")
    pdf.ln(10) 
                 
       # Create subplot and bar
    fig, ax = plt.subplots()
    ax.plot(datos['fecha_desde'].values, datos['total'].values, color="#E63946", marker='D', label = 'Total Ventas') 
    ax.plot(datos['fecha_desde'].values, datos['pagado'].values, color="#508D69", marker='D', label = 'Total Pagos', dashes = [2,2]) 

    # Set Title
    ax.set_title('Comparación Ventas / Pagos', fontweight="bold")

    # Set xticklabels
    ax.set_xticklabels(datos['fecha_desde'].values, rotation=90)
    plt.xticks(datos['fecha_desde'].values)

    # Set ylabel
    ax.set_ylabel('Montos') 
    plt.legend()
    plt.grid()

    # Save the plot as a PNG
    plt.savefig("tmp/reporte_ventas_grafico.png", dpi=300, bbox_inches='tight', pad_inches=0)
    pdf.ln(10)
    pdf.image("tmp/reporte_ventas_grafico.png", w=190)
    
  

    pdf.output("tmp/reporte_ventas.pdf", 'F')

    return send_file('../tmp/reporte_ventas.pdf', mimetype='application/pdf')