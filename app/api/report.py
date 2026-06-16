from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from app.state import REPORT_CACHE
import io

router = APIRouter()


@router.post("/")
def generate_report():

    data = REPORT_CACHE.get("latest", {})

    findings = data.get("findings", [])

    risk = data.get("risk", {})
    recommendations = data.get("recommendations", [])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    elements.append(Paragraph("Enterprise Compliance Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # SUMMARY
    elements.append(Paragraph(
        f"Total Findings: {len(findings)}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # TABLE HEADER
    table_data = [
        ["Rule", "Status", "Confidence", "Evidence", "Reason"]
    ]

    # DYNAMIC ROWS (🔥 FIX)
    for f in findings:
        table_data.append([
            f.get("rule", ""),
            f.get("status", ""),
            str(f.get("confidence", 0)),
            f.get("evidence", "")[:50],
            f.get("reason", "")
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # RISK SECTION
    elements.append(Paragraph(f"Risk Level: {risk}", styles["Normal"]))

    # RECOMMENDATIONS
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Recommendations:", styles["Heading2"]))

    for r in recommendations:
        elements.append(Paragraph(f"- {r}", styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=compliance_report.pdf"
        }
    )