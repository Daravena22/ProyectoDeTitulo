from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.usuario import Usuario   

login = Blueprint('login', __name__, template_folder='templates', static_folder='static', url_prefix='/login')

@login.route("/")
def root():
    return render_template("login.html") 

