from sqlalchemy.orm import Session
from app.models import HistoricalMatch
from app.services.football_data_client import get_team_last_matches


def save_team_history(db: Session, team_name: str, limit: int = 10):
    matches = get_team_last_matches(team_name, limit=limit)

    for m in matches:
        if m["status"] != "FINISHED":
            continue

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        home_goals = m["score"]["fullTime"]["home"]
        away_goals = m["score"]["fullTime"]["away"]

        home_ht = m["score"]["halfTime"]["home"]
        away_ht = m["score"]["halfTime"]["away"]

        db.add(HistoricalMatch(
            team=home,
            opponent=away,
            is_home=True,
            goals_for=home_goals,
            goals_against=away_goals,
            goals_for_ht=home_ht,
            goals_against_ht=away_ht,
            match_date=m["utcDate"][:10],
            status="FINISHED"
        ))

        db.add(HistoricalMatch(
            team=away,
            opponent=home,
            is_home=False,
            goals_for=away_goals,
            goals_against=home_goals,
            goals_for_ht=away_ht,
            goals_against_ht=home_ht,
            match_date=m["utcDate"][:10],
            status="FINISHED"
        ))

    db.commit()
