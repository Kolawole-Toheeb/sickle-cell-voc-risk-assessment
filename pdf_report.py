from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
def generate_pdf(patient_data, prediction, confidence):
    """
    Generate a professional PDF report for the prediction.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(8.27 * inch, 11.69 * inch),  # A4 size
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []
    # ==========================
    # Custom Styles
    # ==========================

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.darkblue

    subtitle_style = styles["Heading2"]
    subtitle_style.alignment = TA_CENTER
    subtitle_style.textColor = colors.darkblue

    normal_style = styles["BodyText"]
        # ==========================
    # Report Header
    # ==========================

    story.append(
        Paragraph(
            "SICKLE CELL VOC RISK ASSESSMENT REPORT",
            title_style,
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(
            "Clinical Decision Support Report",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            "Machine Learning-Based Risk Assessment Tool for Sickle Cell Disease Management",
            normal_style,
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

    story.append(
        Paragraph(
            f"<b>Report Generated:</b> {current_time}",
            normal_style,
        )
    )
    story.append(Spacer(1, 0.30 * inch))

    # ==========================
    # Patient Information
    # ==========================

    story.append(Paragraph("<b>Patient Information</b>", subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    table_data = [["Parameter", "Value"]]

    for key, value in patient_data.items():
        table_data.append([str(key), str(value)])

    table = Table(table_data, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.30 * inch))
    # ==========================
    # Prediction Result
    # ==========================

    story.append(Paragraph("<b>Prediction Result</b>", subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    prediction_data = [
        ["Prediction", prediction],
        ["Confidence", f"{confidence:.2f}%"]
    ]

    prediction_table = Table(prediction_data, colWidths=[220, 220])

    prediction_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(prediction_table)
    story.append(Spacer(1, 0.30 * inch))
    # ==========================
    # Clinical Recommendation
    # ==========================

    story.append(Paragraph("<b>Clinical Recommendation</b>", subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    if prediction == "Low Risk":
        recommendation = (
            "Continue routine follow-up, maintain adequate hydration, "
            "adhere to prescribed medications, and attend regular clinic visits."
        )

    elif prediction.lower() == "medium":
        recommendation = (
            "Patient requires closer monitoring. Ensure medication adherence, "
            "adequate hydration, prompt treatment of infections, and regular follow-up."
        )

    else:
        recommendation = (
            "Patient is at high risk of vaso-occlusive crisis. Immediate clinical "
            "evaluation and close monitoring are recommended. Consider specialist review "
            "and appropriate interventions."
        )

    story.append(Paragraph(recommendation, normal_style))
    story.append(Spacer(1, 0.30 * inch))
    doc.build(story)
    buffer.seek(0)
    return buffer