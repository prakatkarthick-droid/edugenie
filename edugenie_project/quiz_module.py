"""Generate exactly three multiple-choice questions with four options each."""
import json
import re
from ai_client import generate_text

def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("["), text.rfind("]")
    if start >= 0 and end > start:
        return text[start:end + 1]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        return text[start:end + 1]
    return text

def generate_quiz(source_text: str, level: str = "Beginner") -> list[dict]:
    prompt = f'''Create exactly 3 educational multiple-choice questions based on the material below for a {level} learner.
Return ONLY valid JSON as an array. Each item must have: "question" (string), "options" (array of exactly 4 strings), "answer" (one option string copied exactly from options), and "explanation" (brief string).
Material:\n{source_text}'''
    raw = generate_text(prompt)
    data = json.loads(clean_json_block(raw))
    if isinstance(data, dict):
        data = data.get("questions", [])
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Expected a JSON array containing exactly three questions.")
    normalized = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each quiz item must be an object.")
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()
        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError("Every question must have text and exactly four options.")
        options = [str(option).strip() for option in options]
        if answer not in options:
            raise ValueError("The correct answer must exactly match one of the four options.")
        normalized.append({"question": question, "options": options, "answer": answer, "explanation": explanation})
    return normalized
