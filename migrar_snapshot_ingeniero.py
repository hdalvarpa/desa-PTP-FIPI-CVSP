from app import app
from models.database import db
from models.constatacion import Constatacion
from models.informe_tecnico import InformeTecnico
from models.beneficiario_jefe import BeneficiarioJefe
from models.proyecto import Proyecto

def migrar_snapshot():
    with app.app_context():
        # Añadir columnas si no existen
        from sqlalchemy import text
        try:
            db.session.execute(text('ALTER TABLE constatacion ADD COLUMN id_ingeniero INTEGER REFERENCES ingeniero(id_ingeniero) ON DELETE SET NULL;'))
            db.session.commit()
            print("Columna id_ingeniero agregada a constatacion.")
        except Exception as e:
            db.session.rollback()
            print("Constatacion: " + str(e))
            
        try:
            db.session.execute(text('ALTER TABLE informe_tecnico ADD COLUMN id_ingeniero INTEGER REFERENCES ingeniero(id_ingeniero) ON DELETE SET NULL;'))
            db.session.commit()
            print("Columna id_ingeniero agregada a informe_tecnico.")
        except Exception as e:
            db.session.rollback()
            print("InformeTecnico: " + str(e))
            
        # Update constatacion
        sql_update_c = text("""
            UPDATE constatacion c
            SET id_ingeniero = ip.id_ingeniero
            FROM beneficiario_jefe b
            JOIN ingeniero_proyecto ip ON b.id_proyecto = ip.id_proyecto AND ip.estado_activo = TRUE
            WHERE c.id_beneficiario_jefe = b.id_beneficiario_jefe
              AND c.id_ingeniero IS NULL
        """)
        res_c = db.session.execute(sql_update_c)
        
        # Update informe_tecnico
        sql_update_i = text("""
            UPDATE informe_tecnico i
            SET id_ingeniero = ip.id_ingeniero
            FROM beneficiario_jefe b
            JOIN ingeniero_proyecto ip ON b.id_proyecto = ip.id_proyecto AND ip.estado_activo = TRUE
            WHERE i.id_beneficiario_jefe = b.id_beneficiario_jefe
              AND i.id_ingeniero IS NULL
        """)
        res_i = db.session.execute(sql_update_i)
        
        db.session.commit()
        print(f"Migración completa. Constataciones actualizadas: {res_c.rowcount}. Informes actualizados: {res_i.rowcount}")

if __name__ == '__main__':
    migrar_snapshot()
