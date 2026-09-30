from ai_client import generate_text

def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = ("Create a personalized learning path for the topic below. Organize it from beginner to "
              "intermediate to advanced. Include a suggested timeline, prerequisites, weekly milestones, "
              "practice projects, and useful resource types or reputable resource names. Do not invent exact "
              "URLs. Adapt the starting point to the learner's current level.\n"
              f"Topic: {topic}\nCurrent level: {level}")
    return generate_text(prompt)
