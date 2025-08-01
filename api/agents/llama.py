import httpx

def generate_llama_response(prompt, model="llama3.2"):
    if not prompt:
        return "⚠️ No prompt provided"

    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = httpx.post(ollama_url, json=payload, timeout=50)
        response.raise_for_status()
        result = response.json().get("response", "")
        if not result:
            print("⚠️ LLaMA response was empty.")
        return result.strip()
    except Exception as e:
        print(f"❌ Error in generate_llama_response: {e}")
        return f"⚠️ Could not generate summary due to error: {e}"