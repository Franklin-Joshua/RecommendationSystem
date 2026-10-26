from utils import ask_ollama

def analyze_profile(profile, model="qwen3:4b"):
    prompt = f"""Analyze this profile briefly:
Interests: {profile['interests']}
Skill: {profile['skill_level']}
Goal: {profile['goal']}
Category: {profile['preferred_category']}

Return 5 short lines:
Primary interests, skill level, goal, preference, constraints.
"""
    return ask_ollama(prompt, model, 0.1)