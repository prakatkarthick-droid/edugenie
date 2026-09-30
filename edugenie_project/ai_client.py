"""Shared Google Gemini client, configured via environment variables."""
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def _client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Copy .env.example to .env and add your Google AI Studio API key.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Gemini SDK is missing. Run: pip install -r requirements.txt") from exc
    return genai.Client(api_key=api_key)

def generate_text(prompt: str) -> str:
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    response = _client().models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise ValueError("Gemini returned an empty response.")
    return text.strip()
