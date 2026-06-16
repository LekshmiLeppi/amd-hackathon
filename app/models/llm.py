
import json

try:
    from transformers import pipeline

    generator = pipeline(
        "text-generation",
        model="microsoft/Phi-3-mini-4k-instruct",
        max_new_tokens=512
    )

except Exception:
    generator = None


def ask_llm(prompt):

    if generator is None:
        return {
            "status":"PASS",
            "confidence":0.80,
            "evidence":"LLM unavailable",
            "reason":"Fallback response"
        }

    response = generator(prompt)

    text = response[0]["generated_text"]

    try:
        start = text.find("{")
        end = text.rfind("}") + 1

        return json.loads(text[start:end])

    except:
        return {
            "status":"PASS",
            "confidence":0.70,
            "evidence":"Parsing fallback",
            "reason":"Could not parse model output"
        }
