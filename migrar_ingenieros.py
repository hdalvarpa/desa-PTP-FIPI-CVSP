from app import app
from models.database import db
from sqlalchemy import text
from datetime import date

def migrar_ingenieros():
    with app.app_context():
        # 1. Crear la tabla `ingeniero_proyecto` si no existe
        from models.ingeniero_proyecto import IngenieroProyecto
        # Nota: Normalmente lo crea db.create_all(), así que llamémoslo.
        db.create_all()

        # 2. Extraer datos actuales de entidad_tecnica y entidad_proyecto usando RAW SQL
        # para no depender del modelo de SQLAlchemy que ya no tiene la columna id_ingeniero_vigente
        sql_fetch = text("""
            SELECT et.id_entidad_tecnica, et.id_ingeniero_vigente, ep.id_proyecto
            FROM entidad_tecnica et
            JOIN entidad_proyecto ep ON et.id_entidad_tecnica = ep.id_entidad_tecnica
            WHERE et.id_ingeniero_vigente IS NOT NULL
        """)
        
        resultados = db.session.execute(sql_fetch).fetchall()
        
        if not resultados:
            print("No hay ingenieros vigentes asignados a entidades técnicas con proyectos para migrar.")
            return

        print(f"Se encontraron {len(resultados)} asociaciones entidad-proyecto con un ingeniero vigente.")

        # 3. Insertar los datos en ingeniero_proyecto
        # Evitamos duplicados por si se corre dos veces (misma combinacion ingeniero-proyecto-activa)
        sql_insert = text("""
            INSERT INTO ingeniero_proyecto (id_ingeniero, id_proyecto, fecha_inicio, estado_activo)
            VALUES (:id_ingeniero, :id_proyecto, :fecha_inicio, :estado_activo)
        """)

        insertados = 0
        for row in resultados:
            id_et, id_ing, id_proy = row
            
            # Chequear si ya existe
            sql_check = text("SELECT 1 FROM ingeniero_proyecto WHERE id_ingeniero = :id_ing AND id_proyecto = :id_proy AND estado_activo = TRUE")
            existe = db.session.execute(sql_check, {'id_ing': id_ing, 'id_proy': id_proy}).fetchone()
            
            if not existe:
                db.session.execute(sql_insert, {
                    'id_ingeniero': id_ing,
                    'id_proyecto': id_proy,
                    'fecha_inicio': date(2026, 6, 1),
                    'estado_activo': True
                })
                insertados += 1
        
        db.session.commit()
        print(f"Migración completada con éxito. Registros insertados: {insertados}")
        
        # 4. (Opcional) Sentencia para borrar la columna vieja
        print("\nPara completar la limpieza, ejecuta manualmente el siguiente DROP:")
        print("ALTER TABLE entidad_tecnica DROP COLUMN id_ingeniero_vigente;")
        # Nota: SQLite no soporta 'DROP COLUMN' en versiones muy antiguas, pero en las recientes sí.
        # Si usas PostgreSQL (Render), esto funcionará perfecto.

if __name__ == '__main__':
    migrar_ingenieros()
