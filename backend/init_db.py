from database import SessionLocal, engine, Base
from models import Usuario, RolEnum
from security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

existe = db.query(Usuario).filter(Usuario.rol == RolEnum.DIRECTOR).first()
if not existe:
    director = Usuario(
        email="director@example.com",
        password=hash_password("director123"),
        nombre="Juan",
        apellido="Director",
        rol=RolEnum.DIRECTOR
    )
    db.add(director)
    db.commit()
    print("✓ Director creado: director@example.com / director123")
else:
    print("✓ Ya existe un director")

db.close()
