import os
import requests
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db
from app.models.league import League
from app.models.match import Match

load_dotenv()

router = APIRouter(prefix="/internal", tags=["internal"])

THESPORTSDB_API_KEY = os.getenv("THESPORTSDB_API_KEY")


@router.post("/sync-matches")
def sync_matches(db: Session = Depends(get_db), season: str = "2023-2024"):

    leagues = db.query(League).filter(League.season == season).all()

    if not leagues:
        return {"message": "No leagues found"}

    total_inserted = 0

    for league in leagues:

        url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/eventsseason.php?id={league.external_id}&s={season}"

        response = requests.get(url)
        data = response.json()

        events = data.get("events")

        if not events:
            continue

        for event in events:

            exists = db.query(Match).filter(
                Match.league_id == league.id,
                Match.home_team == event["strHomeTeam"],
                Match.away_team == event["strAwayTeam"],
                Match.season == season
            ).first()

            if exists:
                continue

            home_goals = int(event["intHomeScore"]) if event.get("intHomeScore") else None
            away_goals = int(event["intAwayScore"]) if event.get("intAwayScore") else None

            # 🔥 CORREÇÃO AQUI
            is_finished = home_goals is not None and away_goals is not None

            btts = False
            over_15 = False
            over_25 = False

            if home_goals is not None and away_goals is not None:
                total_goals = home_goals + away_goals
                btts = home_goals > 0 and away_goals > 0
                over_15 = total_goals > 1
                over_25 = total_goals > 2

            match = Match(
                league_id=league.id,
                home_team=event["strHomeTeam"],
                away_team=event["strAwayTeam"],
                match_date=datetime.strptime(event["dateEvent"], "%Y-%m-%d"),
                season=season,
                is_finished=is_finished,
                home_goals=home_goals,
                away_goals=away_goals,
                btts=btts,
                over_15=over_15,
                over_25=over_25
            )

            db.add(match)
            total_inserted += 1

        db.commit()

    return {
        "status": "ok",
        "inserted_matches": total_inserted,
        "season": season
    }