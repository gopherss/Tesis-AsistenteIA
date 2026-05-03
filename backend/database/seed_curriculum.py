from database.db import SessionLocal
from models.curriculum import (
    Nivel,
    Grado,
    Area,
    Competencia,
    Capacidad,
    Tema
)

db = SessionLocal()


def existe_tabla(model):
    return db.query(model).first() is not None


def seed_niveles():
    if existe_tabla(Nivel):
        return

    primaria = Nivel(nombre="Primaria")
    db.add(primaria)
    db.commit()


def seed_grados():
    if existe_tabla(Grado):
        return

    nivel = db.query(Nivel).filter(Nivel.nombre == "Primaria").first()

    grados = [
        "1ro Primaria",
        "2do Primaria",
        "3ro Primaria",
        "4to Primaria",
        "5to Primaria",
        "6to Primaria",
    ]

    for i, nombre in enumerate(grados, start=1):
        db.add(
            Grado(
                nombre=nombre,
                orden=i,
                nivel_id=nivel.id
            )
        )

    db.commit()


def seed_areas():
    if existe_tabla(Area):
        return

    areas = [
        "Comunicación",
        "Matemática",
        "Ciencia y Tecnología",
        "Personal Social",
        "Arte y Cultura",
        "Tutoría",
        "Inglés",
        "Educación Física",
        "Religión"
    ]

    for nombre in areas:
        db.add(Area(nombre=nombre))

    db.commit()


def seed_competencias():
    if existe_tabla(Competencia):
        return

    data = {
        "Matemática": [
            "Resuelve problemas de cantidad",
            "Resuelve problemas de regularidad, equivalencia y cambio",
            "Resuelve problemas de forma, movimiento y localización",
            "Resuelve problemas de gestión de datos e incertidumbre",
        ],
        "Comunicación": [
            "Se comunica oralmente en su lengua materna",
            "Lee diversos tipos de textos escritos",
            "Escribe diversos tipos de textos",
        ],
        "Ciencia y Tecnología": [
            "Indaga mediante métodos científicos",
            "Explica el mundo físico basándose en conocimientos científicos",
        ],
        "Personal Social": [
            "Construye su identidad",
            "Convive y participa democráticamente",
        ]
    }

    for area_nombre, lista in data.items():
        area = db.query(Area).filter(Area.nombre == area_nombre).first()

        for item in lista:
            db.add(
                Competencia(
                    nombre=item,
                    area_id=area.id
                )
            )

    db.commit()


def seed_temas():
    if existe_tabla(Tema):
        return

    temas_data = {
        "Matemática": [
            "Números naturales",
            "Sumas y restas",
            "Multiplicación",
            "División",
            "Fracciones",
            "Decimales",
            "Perímetro",
            "Área",
            "Estadística básica"
        ],
        "Comunicación": [
            "Comprensión lectora",
            "Tipos de texto",
            "Narración",
            "Descripción",
            "Producción escrita",
            "Ortografía",
            "Exposición oral"
        ],
        "Ciencia y Tecnología": [
            "Los seres vivos",
            "Sistema solar",
            "La materia",
            "Energía",
            "El agua",
            "Experimentos simples"
        ],
        "Personal Social": [
            "La familia",
            "Normas de convivencia",
            "Regiones del Perú",
            "Ciudadanía",
            "Historia del Perú"
        ]
    }

    grados = db.query(Grado).all()

    for grado in grados:
        for area_nombre, lista_temas in temas_data.items():
            area = db.query(Area).filter(Area.nombre == area_nombre).first()

            for tema in lista_temas:
                db.add(
                    Tema(
                        nombre=tema,
                        grado_id=grado.id,
                        area_id=area.id
                    )
                )

    db.commit()

def run():
    print("🌱 Iniciando Seeder...")

    seed_niveles()
    seed_grados()
    seed_areas()
    seed_competencias()
    seed_temas()

    print("✅ Seeder completado correctamente")


if __name__ == "__main__":
    run()