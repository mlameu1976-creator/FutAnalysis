from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import HistoricalMatch
from app.services.football_data_client import football_data_get

router = APIRouter()


@router.post("/historical/load")
def load_historical(league: int = Query(...)):
    db: Session = SessionLocal()

    try:
        params = {
            "competitions": league,
            "status": "FINISHED",
            "limit": 5
        }

        data = football_data_get("/matches", params)

        matches = data.get("matches", [])
        if not matches:
            return {"message": "Nenhum jogo encontrado na API"}

        inserted = 0

        for m in matches:
            if not m.get("score") or not m["score"].get("fullTime"):
                continue

            ft = m["score"]["fullTime"]
            ht = m["score"].get("halfTime", {})

            exists = db.query(HistoricalMatches).filter(
                HistoricalMatches.match_id == m["id"]
            ).first()

            if exists:
                continue

            record = HistoricalMatches(
                match_id=m["id"],
                competition_id=league,
                season=m["season"]["id"],
                home_team=m["homeTeam"]["name"],
                away_team=m["awayTeam"]["name"],
                match_date=m["utcDate"],
                home_goals_ft=ft.get("home", 0),
                away_goals_ft=ft.get("away", 0),
                home_goals_ht=ht.get("home", 0),
                away_goals_ht=ht.get("away", 0)
            )

            db.add(record)
            inserted += 1

        db.commit()
        return {"inserted": inserted}

    finally:
        db.close()
