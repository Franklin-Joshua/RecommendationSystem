def rank_recommendations(recommendations):
    return sorted(recommendations, key=lambda x: x.get("score", 0), reverse=True)
