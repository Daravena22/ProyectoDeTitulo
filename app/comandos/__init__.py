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
    usuario.rut = "12951361-6"
    usuario.clave = generate_password_hash("Nel65412",method="sha256")

    db.session.add(usuario)
    db.session.commit()




