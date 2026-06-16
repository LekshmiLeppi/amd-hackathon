from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
import io

router = APIRouter()


@router.post("/")
def generate_report():

    buffer = io.BytesIO()

    # ----------------------------
    # CREATE REAL PDF
    # ----------------------------
    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, 800, "AI Compliance Audit Report")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, 770, "Status: Generated Successfully")

    pdf.drawString(100, 750, "This is a sample compliance report.")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=audit_report.pdf"
        }
    )