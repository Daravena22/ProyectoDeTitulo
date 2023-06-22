from app import db

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    lugar = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    folios_id = db.Column(db.Integer, db.ForeignKey("folios.id"))
