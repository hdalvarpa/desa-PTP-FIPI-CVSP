from models.database import db

class Ingeniero(db.Model):
    __tablename__ = 'ingeniero'
    
    id_ingeniero = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=True)
    apellido_materno = db.Column(db.String(100), nullable=True)
    cip = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relationships
    asignaciones_proyectos = db.relationship('IngenieroProyecto', backref='ingeniero_rel', lazy=True)
    
    @property
    def esta_disponible(self):
        # Retorna True si no tiene asignaciones activas
        for asignacion in self.asignaciones_proyectos:
            if asignacion.estado_activo:
                return False
        return True

    def __repr__(self):
        return f'<Ingeniero CIP:{self.cip}>'
