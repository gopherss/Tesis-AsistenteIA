from database.db import SessionLocal
from models.curriculum import Grado, Area, Competencia, Capacidad, Tema, Desempeno

db = SessionLocal()

def get_or_create(model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.add(instance)
        db.flush() # Sincroniza para obtener el ID
    return instance

def seed_grados():
    print("  -> Poblando Grados...")
    grados = ["1ro Primaria", "2do Primaria", "3ro Primaria", "4to Primaria", "5to Primaria", "6to Primaria"]
    for i, nombre in enumerate(grados, start=1):
        get_or_create(Grado, nombre=nombre, orden=i)
    db.commit()

def seed_curriculo_base():
    print("  -> Poblando Áreas, Competencias y Capacidades...")
    # Estructura basada en el Programa Curricular de Educación Primaria
    data_maestra = {
        "Personal Social": {
            "Construye su identidad": ["Se valora a sí mismo", "Autorregula sus emociones"],
            "Convive y participa democráticamente": ["Interactúa con todas las personas", "Construye normas y asume acuerdos"],
            "Construye interpretaciones históricas": ["Interpreta críticamente fuentes diversas", "Comprende el tiempo histórico"],
            "Gestiona responsablemente el espacio y el ambiente": ["Comprende las relaciones entre los elementos naturales y sociales", "Genera acciones para conservar el ambiente"],
            "Gestiona responsablemente los recursos económicos": ["Comprende las relaciones entre los elementos del sistema económico", "Toma decisiones económicas y financieras"]
        },
        "Comunicación": {
            "Se comunica oralmente en lengua materna": ["Obtiene información del texto oral", "Infiere e interpreta información del texto oral"],
            "Lee diversos tipos de textos escritos": ["Obtiene información del texto escrito", "Infiere e interpreta información del texto"],
            "Escribe diversos tipos de textos": ["Adecúa el texto a la situación comunicativa", "Organiza y desarrolla las ideas de forma coherente"]
        },
        "Matemática": {
            "Resuelve problemas de cantidad": ["Traduce cantidades a expresiones numéricas", "Comunica su comprensión sobre los números"],
            "Resuelve problemas de regularidad, equivalencia y cambio": ["Traduce datos a expresiones algebraicas", "Comunica su comprensión sobre las relaciones algebraicas"],
            "Resuelve problemas de movimiento, forma y localización": ["Modela objetos con formas geométricas", "Comunica su comprensión sobre las formas"],
            "Resuelve problemas de gestión de datos e incertidumbre": ["Representa datos con gráficos y medidas estadísticas", "Comunica su comprensión de los conceptos estadísticos"]
        },
        "Ciencia y Tecnología": {
            "Indaga mediante métodos científicos para construir conocimientos": ["Problematiza situaciones para hacer indagación", "Diseña estrategias para hacer indagación"],
            "Explica el mundo natural y artificial en base a conocimientos": ["Comprende y usa conocimientos sobre los seres vivos", "Evalúa las implicancias del saber y del quehacer científico"]
        },
        "Arte y cultura": {
            "Aprecia de manera crítica manifestaciones artístico-culturales": ["Percibe manifestaciones artístico-culturales", "Contextualiza manifestaciones artístico-culturales"],
            "Crea proyectos desde los lenguajes artísticos": ["Explora y experimenta los lenguajes artísticos", "Aplica procesos creativos"]
        },
        "Educación Física": {
            "Se desenvuelve de manera autónoma a través de su motricidad": ["Comprende su cuerpo", "Se expresa corporalmente"],
            "Asume una vida saludable": ["Comprende las relaciones entre la actividad física y salud", "Incorpora prácticas que mejoran su calidad de vida"]
        },
        "Educación Religiosa": {
            "Construye su identidad como persona humana, amada por Dios": ["Conoce a Dios y asume su identidad religiosa", "Cultiva y valora las manifestaciones religiosas"],
            "Asume la experiencia el encuentro personal y comunitario con Dios": ["Transforma su entorno desde el encuentro personal con Dios", "Actúa coherentemente en razón de su fe"]
        }
    }

    for area_nom, competencias in data_maestra.items():
        area = get_or_create(Area, nombre=area_nom)
        for comp_nom, capacidades in competencias.items():
            comp = get_or_create(Competencia, nombre=comp_nom, area_id=area.id)
            for cap_nom in capacidades:
                get_or_create(Capacidad, nombre=cap_nom, competencia_id=comp.id)
    db.commit()

def seed_temas_y_desempenos():
    print("  -> Poblando Temas y Desempeños (Ejemplos 1ro Primaria)...")
    # Estructura: Área -> Tema -> Lista de Desempeños
    temas_data = {
        "Matemática": {
            "Números naturales": [
                "Establece relaciones entre datos y acciones de agregar o quitar cantidades hasta 20.",
                "Expresa con diversas representaciones su comprensión del número como índice de conteo."
            ],
            "Formas geométricas": [
                "Establece relaciones entre las formas de los objetos que lo rodean y las formas geométricas bidimensionales.",
                "Expresa con material concreto su comprensión sobre los elementos de las formas (lados, esquinas)."
            ]
        },
        "Comunicación": {
            "Comprensión lectora": [
                "Identifica información explícita que es claramente distinguible de otra en diversas partes del texto.",
                "Deduce características de personajes y objetos, así como el significado de palabras según el contexto."
            ],
            "Producción de textos": [
                "Escribe textos en torno a un tema, agrupando las ideas en oraciones.",
                "Revisa el texto con ayuda del docente para determinar si se ajusta al propósito."
            ]
        },
        "Ciencia y Tecnología": {
            "Los seres vivos": [
                "Describe las características y necesidades de los seres vivos (plantas y animales).",
                "Relaciona las partes externas de los seres vivos con sus funciones específicas."
            ]
        },
        "Personal Social": {
            "La familia": [
                "Describe las características y roles de los miembros de su familia y se reconoce como parte de ella.",
                "Comparte con sus compañeros las costumbres y actividades de su familia."
            ]
        }
    }

    grado_1 = db.query(Grado).filter(Grado.nombre == "1ro Primaria").first()
    
    for area_nom, temas in temas_data.items():
        area = db.query(Area).filter(Area.nombre == area_nom).first()
        if area and grado_1:
            for tema_nom, lista_desempenos in temas.items():
                tema = get_or_create(Tema, nombre=tema_nom, grado_id=grado_1.id, area_id=area.id)
                for desc in lista_desempenos:
                    get_or_create(Desempeno, descripcion=desc, tema_id=tema.id)
    db.commit()

def run():
    print("🌱 Iniciando proceso de carga de datos (Seeder)...")
    try:
        seed_grados()
        seed_curriculo_base()
        seed_temas_y_desempenos()
        print("✅ ¡Éxito! La base de datos ha sido poblada correctamente.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error crítico: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
    