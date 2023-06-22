from flask import Blueprint
from werkzeug.security import generate_password_hash
from app import db
from app.modelos.usuario import Usuario


comandos = Blueprint("comandos", __name__)

@comandos.cli.command("crear-usuario")
def crear_usuario():
    print("Creacion de usuario")
    usuario = Usuario()
    usuario.nombre = "Admin"
    usuario.rut = "0-0"
    usuario.clave = generate_password_hash("admin",method="sha256")

    db.session.add(usuario)
    db.session.commit()




