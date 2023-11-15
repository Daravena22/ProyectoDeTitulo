from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.modelos import importar_modelos
from flask_login import LoginManager
from app.configs.app import AppConfigs
from app.configs.database import DatabaseConfigs
from app.configs.logging import LoggingConfigs

LoggingConfigs.init()

app = Flask(__name__) 

app.config['SECRET_KEY'] = AppConfigs.get_secret_key()

database_uri = DatabaseConfigs.get_uri()
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {'pool_size' : 100, 'pool_recycle' : 280}
db = SQLAlchemy(app)

importar_modelos()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login.root'
login_manager.init_app(app)

from app.modelos.usuario import Usuario
@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

from app.web.home import home 
app.register_blueprint(home)

from app.web.login import login
app.register_blueprint(login)

from app.comandos import comandos
app.register_blueprint(comandos)

from app.web.clientes import clientes
app.register_blueprint(clientes)

from app.api.login import api_login
app.register_blueprint(api_login)

from app.api.clientes import api_clientes
app.register_blueprint(api_clientes)

from app.web.mantenedores.categorias import categorias
app.register_blueprint(categorias)

from app.api.mantenedores.categoria import api_categorias
app.register_blueprint (api_categorias)

from app.web.mantenedores.material import material
app.register_blueprint(material)

from app.api.mantenedores.material import api_material
app.register_blueprint(api_material)

from app.web.productos import productos
app.register_blueprint(productos)

from app.api.productos import api_productos
app.register_blueprint(api_productos)

from app.web.mantenedores.folios import folios
app.register_blueprint(folios)

from app.api.mantenedores.folios import api_folios
app.register_blueprint(api_folios)

from app.json_encoder import CustomJSONEncoder
app.json_encoder = CustomJSONEncoder

from app.web.ventas import ventas
app.register_blueprint(ventas)

from app.api.ventas import api_ventas
app.register_blueprint(api_ventas)

from app.api.mantenedores.tipo_abono import api_tipo_abono
app.register_blueprint(api_tipo_abono)

from app.web.pagos import pagos
app.register_blueprint(pagos)

from app.api.pagos import api_pagos
app.register_blueprint(api_pagos)