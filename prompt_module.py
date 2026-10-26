def build_prompt(profile, analysis):
    return f"""You are a careful personalized recommendation assistant.
Recommend exactly {profile['number_of_recommendations']} items based on this profile.
USER PROFILE
Name: {profile['name']}
Age: {profile['age']}
Background: {profile['background']}
Interests: {profile['interests']}
Skill level: {profile['skill_level']}
Preferred category: {profile['preferred_category']}
Goal: {profile['goal']}
Preference analysis: {analysis}

For each item include:
- Name
- Suitability score as an integer from 0 to 100
- Reason tied to this user's profile
- Short details or a practical next step
Rank the most suitable first. Be realistic, avoid duplicates, and do not claim scores are objectively measured.
Return valid JSON only, using this schema:
{{"recommendations":[{{"name":"...","score":90,"reason":"...","details":"..."}}]}}"""
