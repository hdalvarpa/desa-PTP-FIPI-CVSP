from models.database import db

class Predio(db.Model):
    __tablename__ = 'predio'

    id_predio = db.Column(db.Integer, primary_key=True)
    id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)

    partida_registral = db.Column(db.String(50))
    direccion = db.Column(db.String(255))
    departamento = db.Column(db.String(50))
    provincia = db.Column(db.String(50))
    distrito = db.Column(db.String(50))
    manzana = db.Column(db.String(10))
    lote = db.Column(db.String(10))
    sublote = db.Column(db.String(10))
    centro_poblado = db.Column(db.String(150))
    referencia = db.Column(db.String(255))

    def __repr__(self):
        return f'<Predio {self.direccion}>'