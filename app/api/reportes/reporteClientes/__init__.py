from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from sqlalchemy import or_ , func
import pandas as pd
import dataframe_image as dfi
from app.api.reportes.common import create_letterhead, create_title, write_to_pdf, PDF
from fpdf.fonts import FontFace


api_reporteClientes = Blueprint('api_reporteClientes', __name__, url_prefix='/api/reportes/reporteClientes')


@api_reporteClientes.route("/generar", methods=["GET"])
@login_required
def generar_reporte():

    tipo = request.args.get('tipo')
    rows = db.session.query(Cliente.id,Cliente.rut,Cliente.apellido,Cliente.nombre,Cliente.telefono, Cliente.deuda).filter(or_(tipo=='todos',Cliente.deuda>0)).all()
    
   
    # def color_pos_neg_value(value):
    #     if value < 0:
    #         color = 'green'
    #     elif value > 0:
    #         color = 'red'
    #     else:
    #         color = 'black'
    #     return 'color: %s' % color
    
    # df.rename(columns={'rut':'RUT', 'apellido':'Apellido', 'nombre':'Nombre', 'telefono':'Telefono', 'direccion':'Direccion','deuda':'Deuda'}, inplace=True)

    #     # Apply styling to dataframe
    # styled_df = df.style.format({ 
    #     'Deuda': "{:.0f}",
    #     }).hide(axis='index').applymap(color_pos_neg_value, subset=['Deuda'])
    
    # dfi.export(styled_df, 'tmp/reporte_clientes.png')

    # Global Variables
    TITLE = "Reporte de Clientes"
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
    write_to_pdf(pdf, "Tabla de Clientes que destaca aquellos que presentan deuda:")
    pdf.ln(15)

    # Add table
    # pdf.image("tmp/reporte_clientes.png", w=170)
    # pdf.ln(10)
    estilo_cabecera = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(57, 47, 90))
    estilo_deuda = FontFace(emphasis="BOLD", color=(255, 0, 0))
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
        row.cell('Telefono')
        row.cell('Deuda')
        for data_row in rows:
            row = table.row()
            for col,valor in enumerate(data_row):
                if col == 0: continue
                if col == 5 and valor >0:
                    row.cell(str(valor),style=estilo_deuda)
                else:
                    row.cell(str(valor))

    pdf.output("tmp/reporte_clientes.pdf", 'F')
    # Add some words to PDF
    # write_to_pdf(pdf, "2. The visualisations below shows the trend of total sales for Heicoders Academy and the breakdown of revenue for year 2016:")

    # Add the generated visualisations to the PDF
    # pdf.image("resources/heicoders_annual_sales.png", 5, 200, WIDTH/2-10)
    # pdf.image("resources/heicoders_2016_sales_breakdown.png", WIDTH/2, 200, WIDTH/2-10)
    # pdf.ln(10)


    '''
    Second Page of PDF
    '''

    # Add Page
    # pdf.add_page()

    # Add lettterhead
    # create_letterhead(pdf, WIDTH)

    # # Add some words to PDF
    # pdf.ln(40)
    # write_to_pdf(pdf, "3. In conclusion, the year-on-year sales of Heicoders Academy continue to show a healthy upward trend. Majority of the sales could be attributed to the global sales which accounts for 58.0% of sales in 2016.")
    # pdf.ln(15)

    # Generate the PDF
    pdf.output("tmp/reporte_clientes.pdf", 'F')

    return send_file('../tmp/reporte_clientes.pdf', mimetype='application/pdf')

