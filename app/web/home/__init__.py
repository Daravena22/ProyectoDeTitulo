from flask import Blueprint, render_template
from flask_login import login_required

home = Blueprint('home', __name__, template_folder='templates', static_folder='static', url_prefix='/home')

@home.route("/")
@login_required
def root():
    return render_template("home.html")