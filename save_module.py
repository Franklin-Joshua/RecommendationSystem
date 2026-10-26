import os, json
from datetime import datetime

def format_recommendations(profile, recommendations):
    lines = ["PERSONALIZED RECOMMENDATIONS", "="*30, f"Saved: {datetime.now():%Y-%m-%d %H:%M:%S}",
             "", "USER PROFILE", json.dumps(profile, indent=2, ensure_ascii=False), "", "RECOMMENDATIONS"]
    for i, rec in enumerate(recommendations, 1):
        lines += [f"{i}. {rec.get('name','Recommendation')}", f"Score: {rec.get('score',0)}%",
                  f"Reason: {rec.get('reason','')}", f"Details: {rec.get('details','')}", ""]
    return "\\n".join(lines)

def save_recommendations(profile, recommendations, feedback=""):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "recommendations.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(format_recommendations(profile, recommendations))
        if feedback:
            f.write(f"\\nUser feedback: {feedback}\\n")
        f.write("\\n" + "-"*70 + "\\n")
    return path
