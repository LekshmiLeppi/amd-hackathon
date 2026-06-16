import json
import re
from app.models.llm import ask_llm


class ComplianceAgent:

    @staticmethod
    def evaluate(document_text, rules):

        # ----------------------------
        # FORMAT RULES
        # ----------------------------
        rules_text = "\n".join(
            [f"{i+1}. {r}" for i, r in enumerate(rules)]
        )

        # ----------------------------
        # STRICT PROMPT (FIXED)
        # ----------------------------
        prompt = f"""
You are a STRICT insurance compliance engine.

CRITICAL RULES:
- You MUST NOT write explanations outside JSON
- You MUST NOT generate code
- You MUST return ONLY valid JSON array
- No markdown, no text, no commentary

You evaluate rules based on MEANING (semantic matching allowed).

---

RULES:
{rules_text}

---

DOCUMENT:
{document_text[:3000]}

---

TASK:
For each rule:
- Check if required information exists in document
- Use semantic understanding (synonyms allowed)
- If found → PASS
- If not found → FAIL

---

OUTPUT FORMAT (ONLY THIS JSON):

[
  {{
    "rule": "rule text",
    "status": "PASS or FAIL",
    "confidence": 0.0,
    "evidence": "exact match or closest phrase from document",
    "reason": "short explanation"
  }}
]

DO NOT OUTPUT ANYTHING ELSE.
"""

        # ----------------------------
        # CALL LLM
        # ----------------------------
        response = ask_llm(prompt)

        text = str(response).strip()

        # ----------------------------
        # STRONG JSON EXTRACTION (FIXED)
        # ----------------------------
        try:
            # remove any accidental text before/after JSON
            start = text.find("[")
            end = text.rfind("]") + 1

            if start == -1 or end == 0:
                raise ValueError("No JSON array found")

            json_str = text[start:end]

            result = json.loads(json_str)

            # validate structure
            if isinstance(result, list):
                cleaned = []
                for r in result:
                    if isinstance(r, dict):
                        cleaned.append(r)
                return cleaned

        except Exception as e:
            pass

        # ----------------------------
        # SAFE FALLBACK
        # ----------------------------
        return [
            {
                "rule": "SYSTEM_ERROR",
                "status": "FAIL",
                "confidence": 0.0,
                "evidence": text[:500],
                "reason": "Invalid or non-JSON LLM output"
            }
        ]