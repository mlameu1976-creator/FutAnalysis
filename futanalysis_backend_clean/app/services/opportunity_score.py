def opportunity_score(prediction: dict, market: str):
    probs = prediction["probabilities"]
    home_xg = prediction["home_xg"]
    away_xg = prediction["away_xg"]
    total_xg = home_xg + away_xg

    if market not in probs:
        return None

    base_prob = probs[market]

    # fator de confiança pelo volume ofensivo
    confidence = min(total_xg / 3, 1)

    score = base_prob * confidence * 100
    return round(score, 1)
