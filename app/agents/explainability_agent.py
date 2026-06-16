
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
