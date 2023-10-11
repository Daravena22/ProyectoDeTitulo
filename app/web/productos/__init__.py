from flask import Blueprint, render_template
from flask_login import login_required

productos = Blueprint('productos', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/prodcutos', url_prefix='/productos')

@productos.route("/")
@login_required
def root():
    return render_template("productos.html")