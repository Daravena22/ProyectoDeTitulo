from flask import Blueprint, render_template
from flask_login import login_required

categorias = Blueprint('categorias', __name__, template_folder='templates', static_folder='static', url_prefix='/mantenedores/categorias')

@categorias.route("/")
@login_required
def root():
    return render_template("categorias.html")