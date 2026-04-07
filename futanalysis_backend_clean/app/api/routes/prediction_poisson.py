from fastapi import APIRouter, Query
from math import exp, factorial
from app.services.football_data_client import football_data_get

router = APIRouter()


def poisson_prob(lmbda, k):
    return (exp(-lmbda) * (lmbda ** k)) / factorial(k)


@router.get("/prediction/poisson")
def predict_poisson(
    league: int = Query(..., description="Competition ID")
):
    data = football_data_get("/matches", {"competition": league})
    matches = data.get("matches", [])

    valid = [
        m for m in matches
        if m["score"]["fullTime"]["home"] is not None
    ]

    if not valid:
        return {}

    total_games = len(valid)
    home_goals = sum(m["score"]["fullTime"]["home"] for m in valid)
    away_goals = sum(m["score"]["fullTime"]["away"] for m in valid)

    lambda_home = home_goals / total_games
    lambda_away = away_goals / total_games

    # Distribuição de gols (0–4)
    max_goals = 4
    dist_home = {i: round(poisson_prob(lambda_home, i), 4) for i in range(max_goals + 1)}
    dist_away = {i: round(poisson_prob(lambda_away, i), 4) for i in range(max_goals + 1)}

    # Over 2.5
    over25_prob = 0
    btts_prob = 0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson_prob(lambda_home, h) * poisson_prob(lambda_away, a)
            if h + a > 2:
                over25_prob += p
            if h > 0 and a > 0:
                btts_prob += p

    confidence = round(
        ((lambda_home + lambda_away) / 4 + over25_prob + btts_prob) * 33,
        1,
    )

    return {
        "league": league,
        "matches_analyzed": total_games,
        "lambda_home": round(lambda_home, 2),
        "lambda_away": round(lambda_away, 2),
        "prob_over_25": round(over25_prob * 100, 1),
        "prob_btts": round(btts_prob * 100, 1),
        "goal_distribution": {
            "home": dist_home,
            "away": dist_away,
        },
        "confidence_score": confidence,
    }
