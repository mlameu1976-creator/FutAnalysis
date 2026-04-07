from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity
from app.models.pre_match_features import PreMatchFeatures
from app.models.match import Match
from app.models.league import League

from app.services.opportunity_engine import (
    prob_over_15,
    prob_over_25,
    prob_btts,
    prob_goal_ht,
    prob_home_win,
    prob_away_win,
)


MIN_PROBABILITY = 0.60

# 🔥 TODOS OS MERCADOS
ALL_MARKETS = [
    "OVER_1.5",
    "OVER_2.5",
    "UNDER_2.5",
    "BTTS",
    "GOAL_HT",
    "HOME_WIN",
    "AWAY_WIN",
]


def run_opportunity_pipeline(db: Session):

    print("Gerando oportunidades (multi-market completo)...")

    db.query(Opportunity).delete()
    db.commit()

    features = db.query(PreMatchFeatures).all()
    matches = db.query(Match).all()
    leagues = db.query(League).all()

    match_map = {m.id: m for m in matches}
    league_map = {l.external_id: l.name for l in leagues}

    unique_features = {f.match_id: f for f in features}
    features = list(unique_features.values())

    opportunities = []

    for f in features:

        match = match_map.get(f.match_id)
        if not match:
            continue

        league_name = league_map.get(match.league_id, "UNKNOWN")

        home_lambda = getattr(f, "exp_home_goals", None)
        away_lambda = getattr(f, "exp_away_goals", None)

        if not home_lambda or not away_lambda:
            continue

        total_lambda = home_lambda + away_lambda

        # ===============================
        # CALCULO DOS MERCADOS
        # ===============================
        market_probs = {
            "OVER_1.5": prob_over_15(total_lambda),
            "OVER_2.5": prob_over_25(total_lambda),
            "UNDER_2.5": 1 - prob_over_25(total_lambda),
            "BTTS": prob_btts(home_lambda, away_lambda),
            "GOAL_HT": prob_goal_ht(home_lambda, away_lambda),
            "HOME_WIN": prob_home_win(home_lambda, away_lambda),
            "AWAY_WIN": prob_away_win(home_lambda, away_lambda),
        }

        # ===============================
        # FILTRO POR PROBABILIDADE
        # ===============================
        candidates = [
            (m, p)
            for m, p in market_probs.items()
            if p >= MIN_PROBABILITY
        ]

        if not candidates:
            continue

        # ===============================
        # 🔥 EVITAR CONFLITOS
        # ===============================
        has_over = any(m.startswith("OVER") for m, _ in candidates)
        has_under = any(m.startswith("UNDER") for m, _ in candidates)

        if has_over and has_under:
            # mantém apenas o melhor entre over e under
            best_ou = max(
                [(m, p) for m, p in candidates if "OVER" in m or "UNDER" in m],
                key=lambda x: x[1]
            )
            candidates = [
                (m, p) for m, p in candidates
                if m not in ["OVER_1.5", "OVER_2.5", "UNDER_2.5"]
            ]
            candidates.append(best_ou)

        # ===============================
        # 🔥 SELEÇÃO FINAL
        # ===============================
        candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:3]

        for market, prob in candidates:

            opportunities.append({
                "match_id": match.id,
                "market": market,
                "probability": round(prob * 100, 2),
                "league_name": league_name
            })

    if opportunities:
        db.bulk_insert_mappings(Opportunity, opportunities)
        db.commit()

    print(f"Oportunidades geradas: {len(opportunities)}")

    return len(opportunities)