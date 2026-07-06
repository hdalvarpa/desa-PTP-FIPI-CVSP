from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Añadir restricción UNIQUE al id_proyecto en la tabla entidad_proyecto
            db.session.execute(text("""
                ALTER TABLE entidad_proyecto 
                ADD CONSTRAINT unique_id_proyecto UNIQUE (id_proyecto);
            """))
            db.session.commit()
            print("Migration successful")
        except Exception as e:
            db.session.rollback()
            print(f"Migration failed: {e}")

if __name__ == '__main__':
    migrate()
