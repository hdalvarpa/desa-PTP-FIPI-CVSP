from models.database import db
from models.entidad_proyecto import entidad_proyecto

class EntidadTecnica(db.Model):
    __tablename__ = 'entidad_tecnica'
    
    id_entidad_tecnica = db.Column(db.Integer, primary_key=True)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    razon_social = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    rep_dni = db.Column(db.String(20), nullable=False)
    rep_nombres = db.Column(db.String(100), nullable=False)
    rep_apellido_paterno = db.Column(db.String(100), nullable=True)
    rep_apellido_materno = db.Column(db.String(100), nullable=True)
    url_logo = db.Column(db.String(500), nullable=True)
    

    
    # Relationships
    proyectos = db.relationship('Proyecto', secondary=entidad_proyecto, backref='entidades_tecnicas')


    
    def __repr__(self):
        return f'<EntidadTecnica {self.razon_social}>'
