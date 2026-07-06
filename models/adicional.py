from models.database import db

class Adicional(db.Model):
    __tablename__ = 'adicional'

    id_adicional = db.Column(db.Integer, primary_key=True)
    id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)

    nombres = db.Column(db.String(100))
    ap_paterno = db.Column(db.String(50))
    ap_materno = db.Column(db.String(50))
    dni = db.Column(db.String(20))
    vinculo = db.Column(db.String(50))

    def __repr__(self):
        return f'<Adicional {self.dni}>'
