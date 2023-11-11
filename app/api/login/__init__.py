from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.usuario import Usuario 
import logging  

logger = logging.getLogger('app.api.login')

api_login = Blueprint('api_login', __name__, url_prefix='/api/login')


@api_login.route("/dologin", methods=["POST"])
def dologin():
    rut = request.form.get("rut")
    clave = request.form.get("clave")

    usuario = db.session.query(Usuario).filter(Usuario.rut == rut).first()
    if usuario is None:
        return redirect(url_for("login.root"))
    if not check_password_hash(usuario.clave, clave):
        return redirect(url_for("login.root"))
    login_user(usuario)
    logger.info('usuario logueado: '+ rut)
    return redirect(url_for("home.root"))

@api_login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login.root"))
