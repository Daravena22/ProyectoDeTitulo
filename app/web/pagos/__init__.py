from flask import Blueprint, render_template
from flask_login import login_required

pagos = Blueprint('pagos', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/pagos', url_prefix='/pagos')

@pagos.route("/")
@login_required
def root():
    return render_template("pagos.html")