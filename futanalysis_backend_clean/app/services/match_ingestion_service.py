from app.database import SessionLocal
from app.models import HistoricalMatch


def ingest_matches(matches: list):
    db = SessionLocal()

    for match in matches:
        record = HistoricalMatch(
            match_date=match["date"],
            home_team=match["home_team"],
            away_team=match["away_team"],
            home_goals=match["home_goals"],
            away_goals=match["away_goals"],
            home_goals_ht=match["home_goals_ht"],
            away_goals_ht=match["away_goals_ht"],
        )

        db.add(record)

    db.commit()
    db.close()
