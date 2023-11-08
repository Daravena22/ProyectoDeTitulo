from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(30))
    nombre = db.Column(db.String(30))
    detalle = db.Column(db.String(30))
    precio = db.Column(db.Double)
    stock = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"))
    