from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
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



api_reportes = Blueprint('api_reportes', __name__, url_prefix='/api/reportes')


@api_reportes.route("/generar", methods=["GET"])
@login_required
def generar_reporte():

    rows = db.session.query(Cliente.rut,Cliente.apellido,Cliente.nombre,Cliente.telefono,Cliente.direccion, Cliente.deuda).all()
    df = pd.DataFrame([r._asdict() for r in rows])
   
    def color_pos_neg_value(value):
        if value < 0:
            color = 'green'
        elif value > 0:
            color = 'red'
        else:
            color = 'black'
        return 'color: %s' % color
    
    df.rename(columns={'rut':'RUT', 'apellido':'Apellido', 'nombre':'Nombre', 'telefono':'Telefono', 'direccion':'Direccion','deuda':'Deuda'}, inplace=True)

        # Apply styling to dataframe
    styled_df = df.style.format({ 
        'Deuda': "{:.2f}",
        }).hide(axis='index').applymap(color_pos_neg_value, subset=['Deuda'])
    
    dfi.export(styled_df, 'tmp/reporte_clientes.png')

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
    pdf.image("tmp/reporte_clientes.png", w=170)
    pdf.ln(10)

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


def create_letterhead(pdf, WIDTH):
    pdf.image("./app/static/Imagenes/pdf_header.png", 0, 0, WIDTH)

def create_title(title, pdf):
    
    # Add main title
    pdf.set_font('Helvetica', 'b', 20)  
    pdf.ln(40)
    pdf.write(5, title)
    pdf.ln(10)
    
    # Add date of report
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(r=128,g=128,b=128)
    today = time.strftime("%d/%m/%Y")
    pdf.write(4, f'{today}')
    
    # Add line break
    pdf.ln(10)

def write_to_pdf(pdf, words):
    
    # Set text colour, font size, and font type
    pdf.set_text_color(r=0,g=0,b=0)
    pdf.set_font('Helvetica', '', 12)
    
    pdf.write(5, words)

class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Página ' + str(self.page_no()), 0, 0, 'C')

