from datetime import datetime
from sqlalchemy.orm import Session
from app.services.football_data_client import football_data_get
from app.models import HistoricalMatch

def ingest_finished_matches(db: Session, league: int, limit: int = 50):
    params = {
        "competitions": league,
        "status": "FINISHED",
        "limit": limit
    }

    data = football_data_get("/matches", params)
    matches = data.get("matches", [])

    for m in matches:
        ft = m["score"]["fullTime"]
        ht = m["score"]["halfTime"]

        home = ft["home"]
        away = ft["away"]

        if home is None or away is None:
            continue

        exists = db.query(HistoricalMatch).filter_by(
            competition_id=league,
            home_team=m["homeTeam"]["name"],
            away_team=m["awayTeam"]["name"],
            match_date=datetime.fromisoformat(m["utcDate"]).date()
        ).first()

        if exists:
            continue

        match = HistoricalMatch(
            competition_id=league,
            season=m["season"]["id"],
            home_team=m["homeTeam"]["name"],
            away_team=m["awayTeam"]["name"],
            match_date=datetime.fromisoformat(m["utcDate"]).date(),

            home_goals_ft=home,
            away_goals_ft=away,
            home_goals_ht=ht["home"] or 0,
            away_goals_ht=ht["away"] or 0,

            btts=home > 0 and away > 0,
            over_15=(home + away) >= 2,
            over_25=(home + away) >= 3,

            home_win=home > away,
            away_win=away > home,
            draw=home == away
        )

        db.add(match)

    db.commit()
