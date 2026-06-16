
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
