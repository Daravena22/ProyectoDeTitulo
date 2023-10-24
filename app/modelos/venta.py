from app import db

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    lugar = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    folio = db.Column(db.String(15))
    monto_neto = db.Column(db.Double)
    monto_bruto = db.Column(db.Double)
    monto_impuesto = db.Column(db.Double)