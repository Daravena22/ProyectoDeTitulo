from flask import Blueprint
from werkzeug.security import generate_password_hash
from app import db
from app.modelos.usuario import Usuario
from app.modelos.tipo_abono import Tipo_abono
import logging

logger = logging.getLogger("app.comandos")
comandos = Blueprint("comandos", __name__)


@comandos.cli.command("crear-usuario")
def crear_usuario():
    logger.info('Crear Usuario')
    usuario = Usuario()
    usuario.nombre = "Admin"
    usuario.rut = "12951361-6"
    usuario.clave = generate_password_hash("Nel65412",method="sha256")

    db.session.add(usuario)
    db.session.commit()


@comandos.cli.command("iniciar-maestros")
def iniciar_maestro():
    logger.info('Iniciar Maestros')
    tipo_abono = Tipo_abono()
    tipo_abono.nombre = 'Transferencia'
    db.session.add(tipo_abono)
    
    tipo_abono = Tipo_abono()
    tipo_abono.nombre = 'Efectivo'
    db.session.add(tipo_abono)
    db.session.commit()

