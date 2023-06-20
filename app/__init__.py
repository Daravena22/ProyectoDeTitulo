from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.modelos import importar_modelos

app = Flask(__name__) 

database_uri = "mysql+pymysql://root:65412@localhost:3306/NellyJoyas"
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {'pool_size' : 100, 'pool_recycle' : 280}
db = SQLAlchemy(app)

importar_modelos()
migrate = Migrate(app, db)