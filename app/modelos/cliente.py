from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    rut = db.Column(db.String(10))
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50)) 
    telefono = db.Column(db.String(20)) 
    direccion = db.Column(db.String(100))
    deuda = db.Column(db.Double)
    estado = db.Column(db.Double) 

