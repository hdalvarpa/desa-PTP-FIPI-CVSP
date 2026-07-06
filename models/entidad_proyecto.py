from models.database import db

# Tabla de asociación (Muchos a Muchos) entre Entidades Técnicas y Proyectos
entidad_proyecto = db.Table('entidad_proyecto',
    db.Column('id_entidad_tecnica', db.Integer, db.ForeignKey('entidad_tecnica.id_entidad_tecnica', ondelete='CASCADE'), primary_key=True),
    db.Column('id_proyecto', db.Integer, db.ForeignKey('proyecto.id_proyecto', ondelete='CASCADE'), primary_key=True),
    db.Column('fecha_asignacion', db.DateTime, default=db.func.current_timestamp())
)
