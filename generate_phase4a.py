from pathlib import Path

files = {

"app/reports/pdf_generator.py": '''
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    @staticmethod
    def generate(
        output_path,
        result
    ):

        doc = SimpleDocTemplate(
            output_path
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "AI Compliance Audit Report",
                styles["Title"]
            )
        )

        story.append(Spacer(1,12))

        story.append(
            Paragraph(
                f"Compliance Score: {result['compliance_score']}",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"Risk Level: {result['risk_level']}",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1,12))

        story.append(
            Paragraph(
                "Recommendations",
                styles["Heading1"]
            )
        )

        for rec in result["recommendations"]:
            story.append(
                Paragraph(
                    rec,
                    styles["BodyText"]
                )
            )

        story.append(PageBreak())

        story.append(
            Paragraph(
                "Detailed Findings",
                styles["Heading1"]
            )
        )

        for finding in result["findings"]:

            story.append(
                Paragraph(
                    str(finding),
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1,6)
            )

        doc.build(story)
''',

"app/api/report.py": '''
import os
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.reports.pdf_generator import PDFGenerator

router = APIRouter()

@router.post("/report")

def generate_report():

    sample_result = {

        "compliance_score":85,

        "risk_level":"MEDIUM",

        "recommendations":[
            "Review missing signatures",
            "Verify nominee details"
        ],

        "findings":[
            {
                "rule":"Signature",
                "status":"FAIL"
            }
        ]
    }

    filename = f"{uuid4()}.pdf"

    output_path = os.path.join(
        "reports",
        filename
    )

    PDFGenerator.generate(
        output_path,
        sample_result
    )

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=filename
    )
''',
}

for filepath, content in files.items():

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Phase 4A Generated")
print("Remember to register report router in app/main.py")