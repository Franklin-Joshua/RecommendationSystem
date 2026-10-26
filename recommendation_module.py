import json, re
from utils import ask_ollama

def _parse_json(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise ValueError("The model did not return JSON. Please retry.")
    data = json.loads(match.group(0))
    recs = data.get("recommendations", [])
    if not isinstance(recs, list) or not recs:
        raise ValueError("No recommendations were returned. Please retry.")
    cleaned=[]
    for item in recs:
        try: score=max(0,min(100,int(float(item.get("score", 0)))))
        except (ValueError,TypeError): score=0
        cleaned.append({"name":str(item.get("name","Recommendation")),
                        "score":score,"reason":str(item.get("reason","")),
                        "details":str(item.get("details",""))})
    return cleaned

def generate_recommendations(prompt, model="qwen3:4b"):
    result = ask_ollama(prompt, model, 0.4)
    return _parse_json(result)
