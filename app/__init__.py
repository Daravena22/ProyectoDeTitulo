from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.modelos import importar_modelos
from flask_login import LoginManager

app = Flask(__name__) 

app.config['SECRET_KEY'] = "1234"

database_uri = "mysql+pymysql://root:65412@localhost:3306/NellyJoyas"
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
