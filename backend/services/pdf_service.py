from io import BytesIO
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors


def generar_pdf_sesion(sesion):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    # =========================
    # ESTILOS
    # =========================

    titulo_style = ParagraphStyle(
        name="Titulo",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        spaceAfter=14
    )

    subtitulo_style = ParagraphStyle(
        name="Subtitulo",
        parent=styles["Heading2"],
        spaceAfter=10
    )

    texto_style = ParagraphStyle(
        name="Texto",
        parent=styles["BodyText"],
        leading=18,
        spaceAfter=6
    )

    contenido = []

    # =========================
    # HEADER
    # =========================

    contenido.append(
        Paragraph(
            "SESIÓN DE APRENDIZAJE",
            titulo_style
        )
    )

    contenido.append(Spacer(1, 12))

    contenido.append(
        Paragraph(
            f"<b>Título:</b> {sesion.titulo}",
            texto_style
        )
    )

    contenido.append(
        Paragraph(
            f"<b>Grado:</b> {sesion.grado}",
            texto_style
        )
    )

    contenido.append(
        Paragraph(
            f"<b>Área:</b> {sesion.area}",
            texto_style
        )
    )

    contenido.append(
        Paragraph(
            f"<b>Tema:</b> {sesion.tema}",
            texto_style
        )
    )

    contenido.append(Spacer(1, 10))

    contenido.append(
        Paragraph(
            f"<b>Propósito:</b> {sesion.proposito}",
            texto_style
        )
    )

    contenido.append(Spacer(1, 14))

    # =========================
    # COMPETENCIAS
    # =========================

    contenido.append(
        Paragraph(
            "Competencias",
            subtitulo_style
        )
    )

    if sesion.competencias:

        lista = [
            Paragraph(item.strip(), texto_style)
            for item in sesion.competencias.split(",")
        ]

        contenido.append(
            ListFlowable(
                lista,
                bulletType="bullet"
            )
        )

    contenido.append(Spacer(1, 10))

    # =========================
    # CAPACIDADES
    # =========================

    contenido.append(
        Paragraph(
            "Capacidades",
            subtitulo_style
        )
    )

    if sesion.capacidades:

        lista = [
            Paragraph(item.strip(), texto_style)
            for item in sesion.capacidades.split(",")
        ]

        contenido.append(
            ListFlowable(
                lista,
                bulletType="bullet"
            )
        )

    contenido.append(Spacer(1, 10))

    # =========================
    # DESEMPEÑO
    # =========================

    contenido.append(
        Paragraph(
            "Desempeño",
            subtitulo_style
        )
    )

    if sesion.desempeno:

        lista = [
            Paragraph(item.strip(), texto_style)
            for item in sesion.desempeno.split(",")
        ]

        contenido.append(
            ListFlowable(
                lista,
                bulletType="bullet"
            )
        )

    contenido.append(Spacer(1, 12))

    # =========================
    # CONTENIDO IA
    # =========================

    contenido.append(
        Paragraph(
            "Desarrollo de la Sesión",
            subtitulo_style
        )
    )

    contenido.append(Spacer(1, 8))

    if sesion.contenido_ia:

        lineas = sesion.contenido_ia.split("\n")

        tabla_buffer = []

        for linea in lineas:

            linea = linea.strip()

            if not linea:
                continue

            # =========================
            # IGNORAR ---
            # =========================

            if linea.startswith("---"):
                continue

            # =========================
            # TITULOS ###
            # =========================

            if linea.startswith("###"):

                texto = (
                    linea
                    .replace("#", "")
                    .replace("*", "")
                    .strip()
                )

                contenido.append(
                    Paragraph(
                        f"<b>{texto}</b>",
                        subtitulo_style
                    )
                )

                contenido.append(Spacer(1, 8))

                continue

            # =========================
            # TITULOS **
            # =========================

            if linea.startswith("**") and linea.endswith("**"):

                texto = linea.replace("*", "").strip()

                contenido.append(
                    Paragraph(
                        f"<b>{texto}</b>",
                        texto_style
                    )
                )

                contenido.append(Spacer(1, 6))

                continue

            # =========================
            # LISTAS
            # =========================

            if linea.startswith("- "):

                texto = linea[2:].strip()

                contenido.append(
                    Paragraph(
                        f"• {texto}",
                        texto_style
                    )
                )

                continue

            # =========================
            # TABLAS MARKDOWN
            # =========================

            if "|" in linea:

                # ignorar separador markdown
                if ":---" in linea:
                    continue

                columnas = [
                    col.strip()
                    for col in linea.split("|")
                    if col.strip()
                ]

                if columnas:
                    tabla_buffer.append(columnas)

                continue

            else:

                # renderizar tabla pendiente
                if tabla_buffer:

                    tabla = Table(
                        tabla_buffer,
                        repeatRows=1
                    )

                    tabla.setStyle(TableStyle([
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.lightgrey
                        ),

                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.black
                        ),

                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold"
                        ),

                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            1,
                            colors.black
                        ),

                        (
                            "BACKGROUND",
                            (0, 1),
                            (-1, -1),
                            colors.whitesmoke
                        ),

                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, 0),
                            8
                        ),
                    ]))

                    contenido.append(tabla)
                    contenido.append(Spacer(1, 12))

                    tabla_buffer = []

            # =========================
            # NEGRITAS MARKDOWN
            # =========================

            linea = re.sub(
                r"\*\*(.*?)\*\*",
                r"<b>\1</b>",
                linea
            )

            contenido.append(
                Paragraph(
                    linea,
                    texto_style
                )
            )

            contenido.append(Spacer(1, 5))

        # =========================
        # TABLA FINAL PENDIENTE
        # =========================

        if tabla_buffer:

            tabla = Table(
                tabla_buffer,
                repeatRows=1
            )

            tabla.setStyle(TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),
            ]))

            contenido.append(tabla)

    # =========================
    # FOOTER
    # =========================

    contenido.append(Spacer(1, 20))

    contenido.append(
        Paragraph(
            "Documento generado automáticamente por el sistema educativo IA",
            styles["Italic"]
        )
    )

    # =========================
    # GENERAR PDF
    # =========================

    doc.build(contenido)

    buffer.seek(0)

    return buffer