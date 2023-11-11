from app import db

class Tipo_abono(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    nombre = db.Column(db.String(20))