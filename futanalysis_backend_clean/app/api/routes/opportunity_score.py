from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import HistoricalMatch


router = APIRouter()

LAST_N_MATCHES = 5

WEIGHTS = {
    "over_1_5": 25,
    "over_2_5": 25,
    "btts": 20,
    "ht_goal": 20,
    "win": 10,
}


def confidence_label(score: float) -> str:
    if score >= 70:
        return "ALTA"
    if score >= 50:
        return "MÉDIA"
    return "BAIXA"


@router.get("/opportunity-score")
def get_opportunity_score(
    home_team: str = Query(...),
    away_team: str = Query(...),
    competition_id: int = Query(...),
    season: int = Query(...),
    db: Session = Depends(get_db),
):
    home_matches = (
        db.query(HistoricalMatches)
        .filter(
            HistoricalMatches.home_team == home_team,
            HistoricalMatches.competition_id == competition_id,
            HistoricalMatches.season == season,
        )
        .order_by(desc(HistoricalMatches.id))
        .limit(LAST_N_MATCHES)
        .all()
    )

    away_matches = (
        db.query(HistoricalMatches)
        .filter(
            HistoricalMatches.away_team == away_team,
            HistoricalMatches.competition_id == competition_id,
            HistoricalMatches.season == season,
        )
        .order_by(desc(HistoricalMatches.id))
        .limit(LAST_N_MATCHES)
        .all()
    )

    if not home_matches or not away_matches:
        return {
            "message": "Dados insuficientes para calcular score",
            "home_matches_found": len(home_matches),
            "away_matches_found": len(away_matches),
        }

    def calc_percentages(matches, perspective):
        total = len(matches)
        o15 = o25 = btts = ht = win = 0

        for m in matches:
            total_goals = m.home_goals_ft + m.away_goals_ft

            if total_goals > 1:
                o15 += 1
            if total_goals > 2:
                o25 += 1
            if m.home_goals_ft > 0 and m.away_goals_ft > 0:
                btts += 1
            if (m.home_goals_ht + m.away_goals_ht) > 0:
                ht += 1

            if perspective == "home" and m.home_goals_ft > m.away_goals_ft:
                win += 1
            if perspective == "away" and m.away_goals_ft > m.home_goals_ft:
                win += 1

        return {
            "over_1_5": (o15 / total) * 100,
            "over_2_5": (o25 / total) * 100,
            "btts": (btts / total) * 100,
            "ht_goal": (ht / total) * 100,
            "win": (win / total) * 100,
        }

    home_stats = calc_percentages(home_matches, "home")
    away_stats = calc_percentages(away_matches, "away")

    avg_stats = {
        key: round((home_stats[key] + away_stats[key]) / 2, 2)
        for key in home_stats
    }

    final_score = round(
        sum((avg_stats[key] * WEIGHTS[key]) / 100 for key in WEIGHTS),
        2,
    )

    return {
        "home_team": home_team,
        "away_team": away_team,
        "competition_id": competition_id,
        "season": season,
        "analysis_scope": f"Média últimos {LAST_N_MATCHES} jogos (sem data)",
        "scores": {
            "over_1_5_score": avg_stats["over_1_5"],
            "over_2_5_score": avg_stats["over_2_5"],
            "btts_score": avg_stats["btts"],
            "ht_goal_score": avg_stats["ht_goal"],
            "win_score": avg_stats["win"],
        },
        "final_score": final_score,
        "confidence": confidence_label(final_score),
    }
