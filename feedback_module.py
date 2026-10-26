import json
from utils import ask_ollama
from recommendation_module import _parse_json

def refine_recommendations(profile, recommendations, feedback, model="qwen3:4b"):
    prompt = f"""Refine the recommendation list based on user feedback.
User profile: {profile}
Current recommendations: {json.dumps(recommendations, ensure_ascii=False)}
User feedback: {feedback}
Return valid JSON only in this format:
{{"recommendations":[{{"name":"...","score":90,"reason":"...","details":"..."}}]}}
Keep the same number of items ({profile['number_of_recommendations']}), honor exclusions,
and explain why each item fits the feedback. Scores are estimated suitability, not facts."""
    return _parse_json(ask_ollama(prompt, model, 0.4))
