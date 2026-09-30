from ai_client import generate_text

def summarize_text(text: str, level: str = "Beginner") -> str:
    prompt = ("Summarize the following educational passage accurately for quick revision. Keep the key facts, "
              f"use clear language suitable for a {level} learner, and do not add unsupported facts.\nPassage:\n{text}")
    return generate_text(prompt)
