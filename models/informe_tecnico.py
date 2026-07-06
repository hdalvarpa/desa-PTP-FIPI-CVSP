from models.database import db

class InformeTecnico(db.Model):
    __tablename__ = 'informe_tecnico'
    
    id_informe = db.Column(db.Integer, primary_key=True)
    id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)
    id_ingeniero = db.Column(db.Integer, db.ForeignKey('ingeniero.id_ingeniero', ondelete='SET NULL'), nullable=True)
    
    medida_frente = db.Column(db.Float)
    colindante_frente = db.Column(db.String(150))
    
    medida_derecha = db.Column(db.Float)
    colindante_derecha = db.Column(db.String(150))
    
    medida_izquierda = db.Column(db.Float)
    colindante_izquierda = db.Column(db.String(150))
    
    medida_fondo = db.Column(db.Float)
    colindante_fondo = db.Column(db.String(150))
    
    area_terreno = db.Column(db.Float)
    descripcion = db.Column(db.Text)
    
    ingeniero = db.relationship('Ingeniero', backref='informes_tecnicos', lazy=True)
    
    def __repr__(self):
        return f'<InformeTecnico ID {self.id_informe}>'
