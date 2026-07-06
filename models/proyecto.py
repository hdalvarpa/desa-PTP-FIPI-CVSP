from models.database import db

class Proyecto(db.Model):
    __tablename__ = 'proyecto'
    
    id_proyecto = db.Column(db.Integer, primary_key=True)
    codigo_registro = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    anio = db.Column(db.Integer, nullable=False)
    
    # Relationships
    ingenieros_historico = db.relationship('IngenieroProyecto', backref='proyecto_rel', lazy=True)

    @property
    def ingeniero_actual(self):
        for asignacion in self.ingenieros_historico:
            if asignacion.estado_activo:
                return asignacion
        return None

    def __repr__(self):
        return f'<Proyecto {self.codigo_registro} - {self.anio}>'
