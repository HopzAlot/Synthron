import requests

def generate_llama_response(prompt, model="llama3.2"):
    if not prompt:
        raise ValueError("Prompt is required.")

    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(ollama_url, json=payload)
    response.raise_for_status()  # will raise HTTPError for bad status
    result = response.json().get("response", "")
    return result
