from app import db

class Abono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    tipo_abono_id = db.Column(db.Integer, db.ForeignKey("tipo_abono.id"))