
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
