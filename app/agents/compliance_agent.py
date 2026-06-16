
from app.models.llm import ask_llm


class ComplianceAgent:

    @staticmethod
    def evaluate(document_text, rules):

        results = []

        for rule in rules:

            prompt = f"""
You are a compliance auditor.

Rule:
{rule}

Document:
{document_text[:3000]}

Return ONLY JSON:

{{
 "status":"PASS or FAIL",
 "confidence":0.95,
 "evidence":"found evidence",
 "reason":"why"
}}
"""

            result = ask_llm(prompt)

            results.append({
                "rule": rule,
                **result
            })

        return results
