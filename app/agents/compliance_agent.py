import json
from app.models.llm import ask_llm


class ComplianceAgent:

    @staticmethod
    def extract_json(text: str):

        if not text:
            return None

        start = text.find("[")
        end = text.rfind("]") + 1

        if start == -1 or end <= 0:
            return None

        json_str = text[start:end]

        try:
            return json.loads(json_str)
        except Exception:
            return None


    @staticmethod
    def evaluate(document_text, rules):

        # ----------------------------
        # FORMAT RULES
        # ----------------------------
        rules_text = "\n".join(
            [f"{i+1}. {r}" for i, r in enumerate(rules)]
        )

        # ----------------------------
        # PROMPT
        # ----------------------------
        prompt = f"""
You are a STRICT compliance engine.

RULES:
{rules_text}

DOCUMENT:
{document_text[:3000]}

TASK:
Return ONLY JSON array.

NO explanation.
NO text.

FORMAT:
[
  {{
    "rule": "string",
    "status": "PASS or FAIL",
    "confidence": 0.0,
    "evidence": "string",
    "reason": "string"
  }}
]
"""

        # ----------------------------
        # CALL LLM
        # ----------------------------
        response = ask_llm(prompt)

        # ----------------------------
        # 🔥 CONSOLE LOG (RAW RESPONSE)
        # ----------------------------
        print("\n================ LLM RAW RESPONSE ================")
        print(response)
        print("===================================================\n")

        # ----------------------------
        # HANDLE ERROR DICTS
        # ----------------------------
        if isinstance(response, dict):
            print("❌ LLM returned error dictionary")
            return [
                {
                    "rule": "SYSTEM_ERROR",
                    "status": "FAIL",
                    "confidence": 0.0,
                    "evidence": str(response),
                    "reason": "LLM request failed"
                }
            ]

        text = str(response)

        # ----------------------------
        # PARSE JSON
        # ----------------------------
        result = ComplianceAgent.extract_json(text)

        # ----------------------------
        # 🔥 CONSOLE LOG (PARSED OUTPUT)
        # ----------------------------
        print("\n================ PARSED RESULT ================")
        print(result)
        print("==============================================\n")

        if isinstance(result, list):
            cleaned = [r for r in result if isinstance(r, dict)]
            return cleaned

        # ----------------------------
        # FALLBACK
        # ----------------------------
        print("❌ Failed to parse JSON from LLM output")

        return [
            {
                "rule": "SYSTEM_ERROR",
                "status": "FAIL",
                "confidence": 0.0,
                "evidence": text[:500],
                "reason": "Invalid or non-JSON LLM output"
            }
        ]