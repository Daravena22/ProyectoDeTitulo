from app import db

class Folios(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy