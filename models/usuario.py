from models.database import db
from models.usuario_entidad import usuario_entidad

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column('contrasena_hash', db.String(255), nullable=False)
    estado = db.Column(db.String(20), default='ACTIVO', nullable=False)
    
    # Relación con Entidades Técnicas (Muchos a Muchos)
    entidades = db.relationship('EntidadTecnica', secondary=usuario_entidad, backref=db.backref('usuarios_asignados', lazy='dynamic'))
    

    def __repr__(self):
        return f'<Usuario {self.username}>'
