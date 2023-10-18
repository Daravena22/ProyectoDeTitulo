from flask import Blueprint, render_template
from flask_login import login_required

folios = Blueprint('folios', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/mantenedores/folios', url_prefix='/folios')

@folios.route("/")
@login_required
def root():
    return render_template("folios.html")