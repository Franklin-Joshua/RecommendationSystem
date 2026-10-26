from utils import ask_ollama

def explain_recommendation(profile, recommendation, model="qwen3:4b"):
    prompt = f"""Explain in plain language why this recommendation fits the user.
User profile: {profile}
Recommendation: {recommendation}
Mention relevant interests, skill level, and goal. Do not invent facts."""
    return ask_ollama(prompt, model, 0.3)
