from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from io import BytesIO


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

    # Estilos personalizados
    titulo_style = ParagraphStyle(
        name="Titulo",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitulo_style = ParagraphStyle(
        name="Subtitulo",
        parent=styles["Heading2"],
        spaceAfter=8
    )

    texto_style = styles["Normal"]

    contenido = []

    # =========================
    # HEADER
    # =========================
    contenido.append(Paragraph("SESIÓN DE APRENDIZAJE", titulo_style))
    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph(f"<b>Título:</b> {sesion.titulo}", texto_style))
    contenido.append(Paragraph(f"<b>Grado:</b> {sesion.grado}", texto_style))
    contenido.append(Paragraph(f"<b>Área:</b> {sesion.area}", texto_style))
    contenido.append(Paragraph(f"<b>Tema:</b> {sesion.tema}", texto_style))
    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph(f"<b>Propósito:</b> {sesion.proposito}", texto_style))
    contenido.append(Spacer(1, 12))

    # =========================
    # COMPETENCIAS
    # =========================
    contenido.append(Paragraph("Competencias", subtitulo_style))

    if sesion.competencias:
        lista = [
            Paragraph(item.strip(), texto_style)
            for item in sesion.competencias.split(",")
        ]
        contenido.append(ListFlowable(lista, bulletType="bullet"))

    contenido.append(Spacer(1, 10))

    # =========================
    # CAPACIDADES
    # =========================
    contenido.append(Paragraph("Capacidades", subtitulo_style))

    if sesion.capacidades:
        lista = [
            Paragraph(item.strip(), texto_style)
            for item in sesion.capacidades.split(",")
        ]
        contenido.append(ListFlowable(lista, bulletType="bullet"))

    contenido.append(Spacer(1, 10))

    # =========================
    # DESEMPEÑO
    # =========================
    contenido.append(Paragraph("Desempeño", subtitulo_style))

    if sesion.desempeno:
        lista = [
            Paragraph(item.strip(), texto_style)
            for item in sesion.desempeno.split(",")
        ]
        contenido.append(ListFlowable(lista, bulletType="bullet"))

    contenido.append(Spacer(1, 12))

    # =========================
    # CONTENIDO IA
    # =========================
    contenido.append(Paragraph("Desarrollo de la Sesión", subtitulo_style))

    if sesion.contenido_ia:
        # Limpia saltos de línea para que se vea bien
        partes = sesion.contenido_ia.split("\n")

        for linea in partes:
            if linea.strip():
                contenido.append(Paragraph(linea.strip(), texto_style))
                contenido.append(Spacer(1, 6))

    # =========================
    # FOOTER SIMPLE
    # =========================
    contenido.append(Spacer(1, 20))
    contenido.append(Paragraph(
        "Documento generado automáticamente por el sistema educativo IA",
        styles["Italic"]
    ))

    # Construir PDF
    doc.build(contenido)

    buffer.seek(0)
    return buffer