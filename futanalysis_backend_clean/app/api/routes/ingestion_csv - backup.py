from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import requests
import csv
import io

from app.database import get_db
from app.models import HistoricalMatch

router = APIRouter(
    prefix="/ingestion-csv",
    tags=["Ingestion CSV"]
)

BASE_URL = "https://www.football-data.co.uk/mmz4281"


@router.post("/matches")
def ingest_matches_from_csv(
    league_code: str = Query(..., example="E0"),
    season: str = Query(..., example="2324"),
    competition_id: int = Query(..., example=39),
    db: Session = Depends(get_db),
):
    """
    Exemplo:
    league_code=E0 (Premier League)
    season=2324 (2023/2024)
    """

    csv_url = f"{BASE_URL}/{season}/{league_code}.csv"

    response = requests.get(csv_url)
    if response.status_code != 200:
        return {
            "error": "Erro ao baixar CSV",
            "url": csv_url,
            "status_code": response.status_code,
        }

    # ✅ CORREÇÃO AQUI
    csv_file = io.StringIO(response.text)
    reader = csv.DictReader(csv_file)

    inserted = 0

    for row in reader:
        try:
            home_team = row["HomeTeam"]
            away_team = row["AwayTeam"]

            home_goals_ft = int(row["FTHG"])
            away_goals_ft = int(row["FTAG"])

            home_goals_ht = int(row.get("HTHG", 0) or 0)
            away_goals_ht = int(row.get("HTAG", 0) or 0)

            exists = (
                db.query(HistoricalMatches)
                .filter(
                    HistoricalMatches.home_team == home_team,
                    HistoricalMatches.away_team == away_team,
                    HistoricalMatches.competition_id == competition_id,
                    HistoricalMatches.season == int(season),
                )
                .first()
            )

            if exists:
                continue

            match = HistoricalMatches(
                competition_id=competition_id,
                season=int(season),
                home_team=home_team,
                away_team=away_team,
                home_goals_ft=home_goals_ft,
                away_goals_ft=away_goals_ft,
                home_goals_ht=home_goals_ht,
                away_goals_ht=away_goals_ht,
            )

            db.add(match)
            inserted += 1

        except Exception:
            continue

    db.commit()

    return {
        "league_code": league_code,
        "season": season,
        "competition_id": competition_id,
        "inserted": inserted,
        "source": csv_url,
    }
