from app import db

class Folios(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    rango_desde = db.Column(db.String(15))
    rango_hasta = db.Column(db.String(15))
    fecha_asignacion = db.Column(db.Date)
    rsapk = db.Column(db.String(1000))
    frma = db.Column(db.String(1000))
    rsask = db.Column(db.String(1000))
    rsapubk =db.Column(db.String(1000))
    ultimo_utilizado =db.Column(db.String(15))
    