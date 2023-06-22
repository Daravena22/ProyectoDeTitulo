from app import db

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    nombre = db.Column(db.String(100))