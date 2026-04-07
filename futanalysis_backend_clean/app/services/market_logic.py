def confidence_from_score(score: int) -> str:
    if score >= 85:
        return "Excelente"
    if score >= 75:
        return "Boa"
    if score >= 65:
        return "Média"
    return "Descartar"


def over_15_logic(stats: dict) -> dict | None:
    score = 0
    reasons = []

    if stats["total_avg_goals"] >= 2.2:
        score += 25
        reasons.append("Média total de gols alta")

    if stats["over_15_rate"] >= 0.7:
        score += 25
        reasons.append("Over 1.5 frequente")

    if stats["home_avg_goals"] >= 1.2 or stats["away_avg_goals"] >= 1.2:
        score += 15
        reasons.append("Time com ataque consistente")

    if score < 65:
        return None

    return {
        "market": "Over 1.5",
        "score": score,
        "confidence": confidence_from_score(score),
        "reasons": reasons,
    }


def over_25_logic(stats: dict) -> dict | None:
    score = 0
    reasons = []

    if stats["total_avg_goals"] >= 2.8:
        score += 30
        reasons.append("Média total muito alta")

    if stats["over_25_rate"] >= 0.6:
        score += 30
        reasons.append("Over 2.5 recorrente")

    if stats["btts_rate"] >= 0.6:
        score += 15
        reasons.append("BTTS frequente")

    if score < 65:
        return None

    return {
        "market": "Over 2.5",
        "score": score,
        "confidence": confidence_from_score(score),
        "reasons": reasons,
    }


def btts_logic(stats: dict) -> dict | None:
    score = 0
    reasons = []

    if stats["btts_rate"] >= 0.65:
        score += 35
        reasons.append("Ambos marcam com frequência")

    if stats["home_avg_goals"] >= 1.1 and stats["away_avg_goals"] >= 1.1:
        score += 30
        reasons.append("Ambos ataques fortes")

    if score < 65:
        return None

    return {
        "market": "BTTS",
        "score": score,
        "confidence": confidence_from_score(score),
        "reasons": reasons,
    }


def ht_goal_logic(stats: dict) -> dict | None:
    score = 0
    reasons = []

    if stats["ht_goal_rate"] >= 0.6:
        score += 40
        reasons.append("Gol no 1º tempo frequente")

    if stats["total_avg_goals"] >= 2.5:
        score += 25
        reasons.append("Jogo com tendência ofensiva")

    if score < 65:
        return None

    return {
        "market": "Gol HT",
        "score": score,
        "confidence": confidence_from_score(score),
        "reasons": reasons,
    }
