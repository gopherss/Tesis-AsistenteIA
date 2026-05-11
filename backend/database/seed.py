import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import SessionLocal, Base, engine
from models.user import Usuario, RolEnum
from security.security import hash_password

# IMPORTANTE: Importar TODOS los modelos para que SQLAlchemy los registre
import models.user
import models.sesion
import models.curriculum
import models.metricas

# Crear las tablas (ahora con todos los modelos registrados)
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    # Verificar si ya hay usuarios
    if db.query(Usuario).count() > 0:
        print("Ya existen usuarios en la base de datos. Seed no ejecutado.")
        db.close()
        return

    # Crear usuario director
    director = Usuario(
        email="director@ejemplo.com",
        password=hash_password("director123"),
        nombre="Carlos",
        apellido="Ramírez",
        rol=RolEnum.DIRECTOR
    )

    # Crear usuario docente
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