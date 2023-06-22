from app import db

class Detalle_venta(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    precio = db.Column(db.String(100))
    unidades = db.Column(db.Integer)
    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"))
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))