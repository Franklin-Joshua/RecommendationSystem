import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


def ask_ollama(prompt, model="qwen3:4b", temperature=0.3,
               max_tokens=512):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "num_ctx": 2048
        }
    }

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=600
    )

    response.raise_for_status()
    return response.json().get("response", "").strip()


def check_ollama(model="qwen3:4b"):
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10
        )
        response.raise_for_status()

        models = [
            item.get("name", "")
            for item in response.json().get("models", [])
        ]

        if any(name == model or name.startswith(model + ":")
               for name in models):
            return True, f"Connected. {model} is installed."

        return False, f"Model {model} is not installed. Run: ollama pull {model}"

    except Exception as e:
        return False, f"Cannot connect to Ollama: {e}"
