from utils import ask_ollama

INTENTS = ["GENERATE_RECOMMENDATION","REFINE_RECOMMENDATION","SHOW_PROFILE",
           "EXPLAIN_RECOMMENDATION","SAVE_RECOMMENDATION","EXIT"]

def detect_intent(user_request, model="qwen3:4b"):
    if not user_request.strip():
        return "UNKNOWN"
    prompt = f"""Classify the user's request into exactly one intent:
{", ".join(INTENTS)}
Return only the intent label.
User request: {user_request}"""
    answer = ask_ollama(prompt, model, 0)
    upper = answer.upper()
    for intent in INTENTS:
        if intent in upper:
            return intent
    return "GENERATE_RECOMMENDATION"
