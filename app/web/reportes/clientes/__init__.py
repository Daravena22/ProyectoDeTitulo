from flask import Blueprint, render_template
from flask_login import login_required

reporteClientes = Blueprint('reporteClientes', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/reportes/reporteClientes', url_prefix='/reporteClientes')

@reporteClientes.route("/")
@login_required
def root():
    return render_template("reporteClientes.html")