from pathlib import Path

files = {

"app/agents/risk_agent.py": '''
class RiskAgent:

    @staticmethod
    def calculate(results):

        total = len(results)

        failed = len([
            r for r in results
            if r["status"] == "FAIL"
        ])

        score = max(
            0,
            100 - (failed * 20)
        )

        if score >= 90:
            level = "LOW"
        elif score >= 70:
            level = "MEDIUM"
        else:
            level = "HIGH"

        return {
            "compliance_score": score,
            "risk_level": level,
            "violations": failed
        }
''',

"app/agents/explainability_agent.py": '''
class ExplainabilityAgent:

    @staticmethod
    def generate(results):

        recommendations = []

        for item in results:

            if item["status"] == "FAIL":

                recommendations.append(
                    f"Review rule: {item['rule']}"
                )

        return recommendations
''',

"app/api/validate.py": '''
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
'''
}

for filepath, content in files.items():

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Phase 3B Generated Successfully")