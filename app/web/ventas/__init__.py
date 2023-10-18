from flask import Blueprint, render_template
from flask_login import login_required

ventas = Blueprint('productos', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/ventas', url_prefix='/ventas')

@ventas.route("/")
@login_required
def root():
    return render_template("ventas.html")