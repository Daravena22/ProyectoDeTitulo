from flask import Blueprint, render_template
from flask_login import login_required

clientes = Blueprint('clientes', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/clientes', url_prefix='/clientes')

@clientes.route("/")
@login_required
def root():
    return render_template("clientes.html")