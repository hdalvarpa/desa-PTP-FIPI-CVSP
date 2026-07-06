from models.database import db
from datetime import datetime

class Constatacion(db.Model):
    __tablename__ = 'constatacion'
    
    id_constatacion = db.Column(db.Integer, primary_key=True)
    id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)
    id_ingeniero = db.Column(db.Integer, db.ForeignKey('ingeniero.id_ingeniero', ondelete='SET NULL'), nullable=True)
    tiene_agua = db.Column(db.Boolean, default=False)
    tiene_saneamiento = db.Column(db.Boolean, default=False)
    
    ingeniero = db.relationship('Ingeniero', backref='constataciones', lazy=True)
    
    def __repr__(self):
        return f'<Constatacion ID {self.id_constatacion}>'
