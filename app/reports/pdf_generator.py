
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
