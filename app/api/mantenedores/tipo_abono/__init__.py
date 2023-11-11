from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.tipo_abono import Tipo_abono 
from app.common.sql_utils import SqlUtils

api_tipo_abono = Blueprint('api_tipo_abono', __name__, url_prefix='/api/mantenedores/tipo_abono')

@api_tipo_abono.route("/listartodo", methods=["GET"])
@login_required
def listar_todos_abono():
    
    rows = db.session.query(Tipo_abono.nombre, Tipo_abono.id).all()
    data = SqlUtils.rows_to_dict(rows)
    
    return jsonify({"data": data})