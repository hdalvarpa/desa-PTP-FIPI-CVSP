from .database import db

class BeneficiarioJefe(db.Model):
    __tablename__ = 'beneficiario_jefe'

    id_beneficiario_jefe = db.Column(db.Integer, primary_key=True)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id_proyecto', ondelete='CASCADE'), nullable=False)
    
    # Datos Ficha Inscripción
    fecha_registro = db.Column(db.DateTime)
    correo_contacto = db.Column(db.String(150))
    telefono_contacto = db.Column(db.String(50))
    
    # Datos Jefe
    nombres = db.Column(db.String(100), nullable=False)
    ap_paterno = db.Column(db.String(100), nullable=False)
    ap_materno = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    nacimiento = db.Column(db.String(50))
    estado_civil = db.Column(db.String(50))
    grado_instruccion = db.Column(db.String(100))
    ocupacion = db.Column(db.String(150))
    discapacidad = db.Column(db.String(50), default='Ninguna')
    sit_laboral = db.Column(db.String(50))
    condicion_eco = db.Column(db.String(50))
    ingreso_mensual = db.Column(db.Numeric(10, 2))

    # Relaciones Satélites
    proyecto = db.relationship('Proyecto', backref=db.backref('beneficiarios', lazy=True, cascade='all, delete-orphan'))
    predio = db.relationship('Predio', backref='beneficiario', uselist=False, cascade='all, delete-orphan')
    conyuge = db.relationship('Conyuge', backref='beneficiario', uselist=False, cascade='all, delete-orphan')
    constatacion = db.relationship('Constatacion', backref='beneficiario', uselist=False, cascade='all, delete-orphan')
    informe = db.relationship('InformeTecnico', backref='beneficiario', uselist=False, cascade='all, delete-orphan')
    cargas = db.relationship('Carga', backref='beneficiario', lazy=True, cascade='all, delete-orphan')
    adicionales = db.relationship('Adicional', backref='beneficiario', lazy=True, cascade='all, delete-orphan')
