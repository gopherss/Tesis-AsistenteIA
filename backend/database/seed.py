import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import SessionLocal, Base, engine
from models.user import Usuario, RolEnum
from security.security import hash_password

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    if db.query(Usuario).count() > 0:
        print("Ya existen usuarios en la base de datos. Seed no ejecutado.")
        db.close()
        return

    director = Usuario(
        email="director@ejemplo.com",
        password=hash_password("director123"),
        nombre="Carlos",
        apellido="Ramírez",
        rol=RolEnum.DIRECTOR
    )

    docente = Usuario(
        email="docente@ejemplo.com",
        password=hash_password("docente123"),
        nombre="María",
        apellido="González",
        rol=RolEnum.DOCENTE
    )

    db.add(director)
    db.add(docente)
    db.commit()
    db.close()
    print("Usuarios de ejemplo creados exitosamente.")

if __name__ == "__main__":
    seed_data()
