from flask import Blueprint, render_template
from flask_login import login_required

material = Blueprint('material', __name__, template_folder='templates', static_folder='static', static_url_path= '/static/material', url_prefix='/material')

@material.route("/")
@login_required
def root():
    return render_template("material.html")