import requests
import json

VLLM_URL = "http://localhost:8000/v1/chat/completions"


def ask_llm(prompt):

    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "system",
                "content": "You are a strict compliance auditor. Return ONLY valid JSON array."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "top_p": 0.1,
        "max_tokens": 512
    }

    response = requests.post(VLLM_URL, json=payload)

    result = response.json()

    return result["choices"][0]["message"]["content"]