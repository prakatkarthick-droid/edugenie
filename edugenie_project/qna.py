from ai_client import generate_text

def answer_question(question: str, level: str = "Beginner") -> str:
    prompt = ("You are EduGenie, an accurate educational assistant. Answer the question directly, "
              f"at a {level} level. Use concise explanations and mention uncertainty when appropriate.\n"
              f"Question: {question}")
    return generate_text(prompt)
