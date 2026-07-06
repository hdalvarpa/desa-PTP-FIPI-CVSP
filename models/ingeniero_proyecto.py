from models.database import db

class IngenieroProyecto(db.Model):
    __tablename__ = 'ingeniero_proyecto'

    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_ingeniero = db.Column(db.Integer, db.ForeignKey('ingeniero.id_ingeniero'), nullable=False)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id_proyecto'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    estado_activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<IngenieroProyecto Ing:{self.id_ingeniero} Proy:{self.id_proyecto} Activo:{self.estado_activo}>'
