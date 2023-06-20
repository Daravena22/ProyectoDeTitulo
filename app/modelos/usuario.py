from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    nombre = db.Column(db.String(100))
    clave = db.Column(db.String(200))
    rut = db.Column(db.String(10)) 
