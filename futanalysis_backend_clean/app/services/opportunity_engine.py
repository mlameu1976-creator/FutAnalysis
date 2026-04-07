import math
from sqlalchemy.orm import Session, joinedload

from app.models.match import Match
from app.models.opportunity import Opportunity
from app.models.pre_match_features import PreMatchFeatures


MIN_PROBABILITY = 0.60


# ===============================
# UTILS
# ===============================
def safe_div(a, b):
    return a / b if b != 0 else 0


def clamp(v, min_v=0.0, max_v=1.0):
    return max(min_v, min(max_v, v))


# ===============================
# POISSON
# ===============================
def poisson(k, lamb):
    return (lamb ** k * math.exp(-lamb)) / math.factorial(k)


def prob_over_15(lamb):
    return 1 - (poisson(0, lamb) + poisson(1, lamb))


def prob_over_25(lamb):
    return 1 - (poisson(0, lamb) + poisson(1, lamb) + poisson(2, lamb))


def prob_btts(home, away):
    p_home0 = poisson(0, home)
    p_away0 = poisson(0, away)
    return 1 - (p_home0 + p_away0 - p_home0 * p_away0)


def prob_home_win(home, away):
    prob = 0
    for h in range(7):
        for a in range(7):
            if h > a:
                prob += poisson(h, home) * poisson(a, away)
    return prob


def prob_away_win(home, away):
    prob = 0
    for h in range(7):
        for a in range(7):
            if a > h:
                prob += poisson(h, home) * poisson(a, away)
    return prob


def prob_goal_ht(home, away):
    lambda_ht = (home + away) * 0.45
    return 1 - math.exp(-lambda_ht)


# ===============================
# VALUE ENGINE
# ===============================
def simulate_market_odds(fair_odds):
    return fair_odds * 1.08


def calculate_ev(prob, odds):
    return (prob * odds) - 1


# ===============================
# CONFIDENCE (100% COMPATÍVEL)
# ===============================
def calculate_confidence(home_lambda, away_lambda):

    total = home_lambda + away_lambda

    # intensidade ofensiva
    intensity_score = clamp(total / 4)  # jogos com mais gols = mais previsíveis

    # equilíbrio (evita jogos caóticos)
    balance = 1 - abs(home_lambda - away_lambda) / max(total, 0.01)
    balance_score = clamp(balance)

    # score final
    confidence = (intensity_score * 0.6) + (balance_score * 0.4)

    return clamp(confidence)


def calculate_final_score(prob, ev, confidence):
    return (
        (ev * 0.5) +
        (confidence * 0.3) +
        (prob * 0.2)
    )


# ===============================
# ENGINE PRINCIPAL
# ===============================
def run_opportunity_engine(db: Session):

    print("Gerando oportunidades (modo profissional)...")

    db.query(Opportunity).delete()
    db.commit()

    features = (
        db.query(PreMatchFeatures)
        .options(joinedload(PreMatchFeatures.match).joinedload(Match.league))
        .all()
    )

    created = 0

    for f in features:

        match = f.match

        if not match:
            continue

        home_lambda = getattr(f, "exp_home_goals", None)
        away_lambda = getattr(f, "exp_away_goals", None)

        if not home_lambda or not away_lambda:
            continue

        total_lambda = home_lambda + away_lambda

        markets = [
            ("OVER_1.5", prob_over_15(total_lambda)),
            ("OVER_2.5", prob_over_25(total_lambda)),
            ("UNDER_2.5", 1 - prob_over_25(total_lambda)),
            ("BTTS", prob_btts(home_lambda, away_lambda)),
            ("GOAL_HT", prob_goal_ht(home_lambda, away_lambda)),
            ("HOME_WIN", prob_home_win(home_lambda, away_lambda)),
            ("AWAY_WIN", prob_away_win(home_lambda, away_lambda)),
        ]

        candidates = []

        for market, prob in markets:

            if prob < MIN_PROBABILITY:
                continue

            fair_odds = safe_div(1, prob)
            market_odds = simulate_market_odds(fair_odds)
            ev = calculate_ev(prob, market_odds)

            confidence = calculate_confidence(home_lambda, away_lambda)

            final_score = calculate_final_score(prob, ev, confidence)

            if final_score < 0.05:
                continue

            candidates.append((market, prob, final_score))

        if not candidates:
            continue

        best = max(candidates, key=lambda x: x[2])

        market, prob, score = best

        db.add(
            Opportunity(
                match_id=match.id,
                market=market,
                probability=round(prob * 100, 2),
                score=round(score * 100, 2)
            )
        )

        created += 1

    db.commit()

    print(f"Oportunidades criadas (qualificadas): {created}")

    return created