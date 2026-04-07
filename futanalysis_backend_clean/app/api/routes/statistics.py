from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.database import get_db
from app.models import HistoricalMatch


router = APIRouter()
LAST_N_MATCHES = 5


@router.get("/statistics")
def get_statistics(
    team: str = Query(...),
    competition_id: int = Query(...),
    season: int = Query(...),
    scope: str = Query("all", regex="^(home|away|all)$"),
    db: Session = Depends(get_db),
):
    filters = [
        HistoricalMatch.competition_id == competition_id,
        HistoricalMatch.season == season,
    ]

    if scope == "home":
        filters.append(HistoricalMatch.home_team == team)
    elif scope == "away":
        filters.append(HistoricalMatch.away_team == team)
    else:
        filters.append(
            or_(
                HistoricalMatch.home_team == team,
                HistoricalMatch.away_team == team,
            )
        )

    matches = (
        db.query(HistoricalMatch)
        .filter(*filters)
        .order_by(desc(HistoricalMatch.id))
        .limit(LAST_N_MATCHES)
        .all()
    )

    if not matches:
        return {"message": "Dados insuficientes", "matches_found": 0}

    total = len(matches)
    over_15 = over_25 = btts = ht_goal = wins = 0

    for m in matches:
        goals = m.home_goals_ft + m.away_goals_ft

        if goals > 1:
            over_15 += 1
        if goals > 2:
            over_25 += 1
        if m.home_goals_ft > 0 and m.away_goals_ft > 0:
            btts += 1
        if (m.home_goals_ht + m.away_goals_ht) > 0:
            ht_goal += 1

        if m.home_team == team and m.home_goals_ft > m.away_goals_ft:
            wins += 1
        if m.away_team == team and m.away_goals_ft > m.home_goals_ft:
            wins += 1

    return {
        "team": team,
        "matches_analyzed": total,
        "over_1_5_pct": round(over_15 / total * 100, 2),
        "over_2_5_pct": round(over_25 / total * 100, 2),
        "btts_pct": round(btts / total * 100, 2),
        "ht_goal_pct": round(ht_goal / total * 100, 2),
        "win_pct": round(wins / total * 100, 2),
    }
