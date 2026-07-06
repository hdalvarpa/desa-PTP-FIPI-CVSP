from models.database import db

class Conyuge(db.Model):
    __tablename__ = 'conyuge'

    id_conyuge = db.Column(db.Integer, primary_key=True)
    id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)

    tiene_conyuge = db.Column(db.Boolean, default=False)
    nombres = db.Column(db.String(100))
    ap_paterno = db.Column(db.String(50))
    ap_materno = db.Column(db.String(50))
    dni = db.Column(db.String(20))
    nacimiento = db.Column(db.String(20))
    estado_civil = db.Column(db.String(20))
    grado_instruccion = db.Column(db.String(100))
    ocupacion = db.Column(db.String(100))
    discapacidad = db.Column(db.String(50))
    sit_laboral = db.Column(db.String(50))
    condicion = db.Column(db.String(50))
    ingreso_mensual = db.Column(db.String(20))

    def __repr__(self):
        return f'<Conyuge {self.dni}>'
