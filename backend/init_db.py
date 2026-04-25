from database import SessionLocal, engine, Base
from models import Usuario, RolEnum
from security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

existe = db.query(Usuario).filter(Usuario.rol == RolEnum.DIRECTOR).first()
if not existe:
    director = Usuario(
        email="director@gmail.com",
        password=hash_password("director123"),
        nombre="Juan",
        apellido="Director",
        rol=RolEnum.DIRECTOR
    )
    docente = Usuario(
        email="docente@gmail.com",
        password=hash_password("docente123"),
        nombre="María",
        apellido="Docente",
        rol=RolEnum.DOCENTE
    )
    db.add(director)
    db.add(docente)
    db.commit()
    print("✓ Director creado: director@gmail.com / director123")
    print("✓ Docente creado: docente@gmail.com / docente123")
else:
    print("✓ Ya existe un director")

db.close()
