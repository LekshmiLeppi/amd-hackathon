import requests

VLLM_URL = "http://localhost:8000/v1/chat/completions"
MODEL_NAME = "llama3"


def ask_llm(prompt, return_raw=False):

    try:
        response = requests.post(
            VLLM_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0
            },
            timeout=120
        )

        result = response.json()

        # ----------------------------
        # OPTION 1: RETURN RAW DEBUG (YOU CAN ENABLE)
        # ----------------------------
        if return_raw:
            return {
                "status_code": response.status_code,
                "response": result
            }

        # ----------------------------
        # OPTION 2: SAFE PARSING (NORMAL MODE)
        # ----------------------------
        if response.status_code != 200:
            return {
                "error": "LLM request failed",
                "details": result
            }

        # check structure safely
        if "choices" not in result:
            return {
                "error": "Invalid LLM response format",
                "raw": result
            }

        # extract content safely
        content = result["choices"][0]["message"]["content"]

        return content

    except Exception as e:
        return {
            "error": str(e)
        }