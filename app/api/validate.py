
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.file_service import FileService
from app.config.settings import settings

from app.agents.document_agent import DocumentAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.risk_agent import RiskAgent
from app.agents.explainability_agent import ExplainabilityAgent

router = APIRouter()

@router.post("/validate")
async def validate(
    file: UploadFile = File(...)
):

    path = FileService.save_file(
        file,
        settings.UPLOAD_DIR
    )

    document_text = DocumentAgent.process(
        path
    )

    rules = RetrievalAgent.retrieve(
        document_text
    )

    findings = ComplianceAgent.evaluate(
        document_text,
        rules
    )

    risk = RiskAgent.calculate(
        findings
    )

    recommendations = (
        ExplainabilityAgent.generate(
            findings
        )
    )

    return {
        "document": file.filename,
        **risk,
        "recommendations": recommendations,
        "findings": findings
    }
