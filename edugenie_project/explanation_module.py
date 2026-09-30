"""Simplified concept explanations, optionally using local LaMini-Flan-T5."""
import os
from functools import lru_cache
from ai_client import generate_text

def _local_explainer(topic: str, level: str) -> str:
    from transformers import pipeline
    generator = _local_pipeline()
    prompt = f"Explain {topic} in simple language for a {level.lower()} student. Include a short example."
    result = generator(prompt, max_new_tokens=180, do_sample=True, temperature=0.7)
    return result[0]["generated_text"].strip()

@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline
    model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model_name, device=-1)

def explain_concept(topic: str, level: str = "Beginner") -> str:
    if os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() in {"1", "true", "yes"}:
        try:
            return _local_explainer(topic, level)
        except Exception:
            # If local model setup/download fails, try the configured cloud model.
            pass
    prompt = ("You are EduGenie, a patient educational tutor. Explain the topic clearly and accurately "
              f"for a {level} learner: {topic}\nUse simple language, a concrete example, and a short takeaway.")
    try:
        return generate_text(prompt)
    except RuntimeError:
        # Useful no-key fallback so the interface can be explored without credentials.
        return (f"{topic.strip()} — To learn this topic, start by defining its key idea, then study one "
                "worked example and try explaining it in your own words. Add a Gemini API key in .env "
                "for a personalized AI-generated explanation.")
