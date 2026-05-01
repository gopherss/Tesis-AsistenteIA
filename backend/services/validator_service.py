import re
import unicodedata
from difflib import get_close_matches
from typing import Dict, List


TEMAS_POR_AREA: Dict[str, List[str]] = {
    "Comunicación": [
        "cuento", "fabula", "noticia", "comprension lectora",
        "texto instructivo", "texto descriptivo",
        "sustantivo", "verbo", "adjetivo",
        "sinonimos", "antonimos", "ortografia"
    ],

    "Matemática": [
        "suma", "resta", "multiplicacion", "division",
        "fracciones", "decimales", "porcentaje",
        "perimetro", "area", "graficos",
        "estadistica", "patrones"
    ],

    "Personal Social": [
        "familia", "comunidad", "regiones del peru",
        "convivencia", "derechos", "deberes",
        "identidad", "simbolos patrios"
    ],

    "Ciencia y Tecnología": [
        "seres vivos", "ecosistema", "cuerpo humano",
        "energia", "agua", "materia", "planetas",
        "sistema solar", "animales", "plantas"
    ],

    "Arte y Cultura": [
        "dibujo", "pintura", "danza",
        "musica", "teatro", "manualidades", "colores"
    ],

    "Educación Religiosa": [
        "jesus", "navidad", "semana santa",
        "valores cristianos", "oracion"
    ],

    "Educación Física": [
        "motricidad", "coordinacion", "juegos",
        "resistencia", "velocidad", "equilibrio"
    ],

    "Inglés": [
        "colors", "numbers", "family",
        "animals", "greetings", "food"
    ],

    "Tutoría": [
        "autoestima", "emociones",
        "bullying", "convivencia",
        "habitos de estudio"
    ],
}

# =====================================================
# Utilidades
# =====================================================

def quitar_tildes(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def limpiar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = quitar_tildes(texto)
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto


# =====================================================
# Corrección ortográfica simple
# =====================================================

PALABRAS_GLOBALES = []
for lista in TEMAS_POR_AREA.values():
    PALABRAS_GLOBALES.extend(lista)


def autocorregir_tema(tema: str) -> str:
    """
    Corrige palabras parecidas:
    divicion -> division
    matematica -> matematica
    fracione -> fracciones
    """
    texto = limpiar(tema)

    candidatos = get_close_matches(
        texto,
        PALABRAS_GLOBALES,
        n=1,
        cutoff=0.72
    )

    if candidatos:
        return candidatos[0].title()

    return tema.title()


# =====================================================
# Detección inteligente área
# =====================================================

def detectar_area_correcta(tema: str) -> str | None:
    tema_user = limpiar(tema)

    for area, lista in TEMAS_POR_AREA.items():
        for palabra in lista:
            if palabra in tema_user:
                return area

    # coincidencia aproximada
    for area, lista in TEMAS_POR_AREA.items():
        candidato = get_close_matches(
            tema_user,
            lista,
            n=1,
            cutoff=0.72
        )
        if candidato:
            return area

    return None


# =====================================================
# Temas sugeridos
# =====================================================

def sugerir_temas(area: str, limite: int = 5) -> List[str]:
    return TEMAS_POR_AREA.get(area, [])[:limite]


# =====================================================
# Validación completa
# =====================================================

def validar_sesion(area: str, tema: str) -> dict:
    """
    Devuelve objeto inteligente
    """

    tema_corregido = autocorregir_tema(tema)
    area_detectada = detectar_area_correcta(tema)

    # Caso correcto
    if area_detectada == area:
        return {
            "ok": True,
            "tema_corregido": tema_corregido,
            "mensaje": "Validación correcta"
        }

    # Caso dudoso
    if area_detectada and area_detectada != area:
        return {
            "ok": False,
            "tema_corregido": tema_corregido,
            "mensaje": f"El tema parece pertenecer a '{area_detectada}'",
            "area_sugerida": area_detectada
        }

    # Sin coincidencia
    return {
        "ok": False,
        "tema_corregido": tema_corregido,
        "mensaje": "No se pudo validar el tema",
        "sugerencias": sugerir_temas(area)
    }