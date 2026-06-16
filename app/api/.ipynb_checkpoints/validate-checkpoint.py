import time
from fastapi import APIRouter, UploadFile, File

from app.services.file_service import FileService
from app.config.settings import settings

from app.agents.document_agent import DocumentAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.risk_agent import RiskAgent
from app.agents.explainability_agent import ExplainabilityAgent

from app.services.rule_loader import load_default_rules
from app.services.rule_engine import RuleEngine
from app.state import REPORT_CACHE

router = APIRouter()


@router.post("/")
async def validate(
    file: UploadFile = File(...),
    rules: UploadFile = File(None)
):

    total_start = time.time()

    print("\n" + "=" * 60)
    print("🚀 VALIDATE REQUEST STARTED")
    print("=" * 60)

    try:
        # ----------------------------
        # STEP 1: SAVE FILE
        # ----------------------------
        print("📥 STEP 1: Saving file...")
        step_start = time.time()

        path = FileService.save_file(file, settings.UPLOAD_DIR)

        print(f"✔ DONE in {time.time() - step_start:.2f}s")

        # ----------------------------
        # STEP 2: EXTRACT TEXT
        # ----------------------------
        print("📄 STEP 2: Extracting document...")
        step_start = time.time()

        document_text = DocumentAgent.process(path)

        print(f"✔ DONE in {time.time() - step_start:.2f}s")
        print(f"📝 Length: {len(document_text)}")

        # ----------------------------
        # STEP 3: LOAD SYSTEM RULES
        # ----------------------------
        print("📚 STEP 3: Loading rules...")
        step_start = time.time()

        system_rules = load_default_rules()

        # ----------------------------
        # STEP 4: LOAD USER RULES
        # ----------------------------
        user_rules = []

        if rules:
            content = rules.file.read().decode("utf-8")
            user_rules = [
                r.strip() for r in content.split("\n") if r.strip()
            ]

        # ----------------------------
        # STEP 5: MERGE RULES
        # ----------------------------
        final_rules = RuleEngine.merge_rules(system_rules, user_rules)

        print(f"✔ Total rules: {len(final_rules)}")
        print(f"✔ System rules: {len(system_rules)}")
        print(f"✔ User rules: {len(user_rules)}")

        # ----------------------------
        # STEP 6: COMPLIANCE CHECK
        # ----------------------------
        print("⚖️ STEP 6: Running compliance check...")
        step_start = time.time()

        findings = ComplianceAgent.evaluate(
            document_text,
            final_rules
        )

        print(f"✔ DONE in {time.time() - step_start:.2f}s")

        # ----------------------------
        # STEP 7: RISK SCORE
        # ----------------------------
        print("⚠️ STEP 7: Risk calculation...")

        risk = RiskAgent.calculate(findings)

        # ----------------------------
        # STEP 8: EXPLANATION
        # ----------------------------
        print("💡 STEP 8: Generating recommendations...")

        recommendations = ExplainabilityAgent.generate(findings)

        # ----------------------------
        # 🔥 IMPORTANT FIX (ADDED ONLY THIS BLOCK)
        # ----------------------------
        REPORT_CACHE["latest"] = {
            "document": file.filename,
            "total_rules": len(final_rules),
            "system_rules": len(system_rules),
            "user_rules": len(user_rules),
            "findings": findings,
            "recommendations": recommendations,
            **risk
        }

        # ----------------------------
        # TOTAL TIME
        # ----------------------------
        total_time = time.time() - total_start

        print("=" * 60)
        print(f"🎯 TOTAL TIME: {total_time:.2f}s")
        print("=" * 60)

        # ----------------------------
        # RESPONSE (UNCHANGED)
        # ----------------------------
        return REPORT_CACHE["latest"]

    except Exception as e:
        print("❌ ERROR:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }