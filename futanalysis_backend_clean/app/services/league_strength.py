from sqlalchemy.orm import Session
from app.models import HistoricalMatch



def league_goal_averages(db: Session, competition_id: int, season: int):
    matches = (
        db.query(HistoricalMatches)
        .filter(
            HistoricalMatches.competition_id == competition_id,
            HistoricalMatches.season == season,
        )
        .all()
    )

    if not matches:
        return 1.0, 1.0

    home_goals = sum(m.home_goals_ft for m in matches)
    away_goals = sum(m.away_goals_ft for m in matches)
    n = len(matches)

    return home_goals / n, away_goals / n
