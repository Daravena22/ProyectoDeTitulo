from flask import Blueprint, render_template
from flask_login import login_required

reportePagos = Blueprint('reportePagos', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/reportes/reportePagos', url_prefix='/reportePagos')

@reportePagos.route("/")
@login_required
def root():
    return render_template("reportePagos.html")