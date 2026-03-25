# models/local_model.py
import subprocess
import json

def query_local_model(prompt):
    """
    Query a local LLM via Ollama (like Phi-2 or Mistral).
    Make sure Ollama is running in background: ollama serve
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "phi", prompt],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[Local AI Error] {e}"
