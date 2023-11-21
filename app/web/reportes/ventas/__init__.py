from flask import Blueprint, render_template
from flask_login import login_required

reporteVentas = Blueprint('reporteVentas', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/reportes/reporteVentas', url_prefix='/reporteVentas')

@reporteVentas.route("/")
@login_required
def root():
    return render_template("reporteVentas.html")