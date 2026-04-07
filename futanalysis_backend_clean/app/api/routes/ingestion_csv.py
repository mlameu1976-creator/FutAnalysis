from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import csv
import io

from app.database import get_db
from app.models import HistoricalMatch


router = APIRouter(prefix="/ingestion-csv", tags=["Ingestion CSV"])

# 🔹 MAPEAMENTO OFICIAL DAS LIGAS (SEM INVENTAR DADOS)
LEAGUES = {
    "E0": {"name": "Premier League", "competition_id": 39},
    "D1": {"name": "Bundesliga 1", "competition_id": 78},
    "D2": {"name": "Bundesliga 2", "competition_id": 79},
    "D3": {"name": "Bundesliga 3", "competition_id": 80},
    "SP1": {"name": "La Liga", "competition_id": 140},
    "I1": {"name": "Serie A Itália", "competition_id": 135},
    "F1": {"name": "Ligue 1", "competition_id": 61},
    "P1": {"name": "Portugal A", "competition_id": 94},
    "N1": {"name": "Holanda A", "competition_id": 88},
    "T1": {"name": "Turquia A", "competition_id": 203},
    "B1": {"name": "Brasil A", "competition_id": 71},
    "B2": {"name": "Brasil B", "competition_id": 72},
}

FOOTBALL_DATA_BASE_URL = "https://www.football-data.co.uk/mmz4281"


@router.post("/matches")
def ingest_matches_from_csv(
    league_code: str,
    season: str,
    db: Session = Depends(get_db),
):
    """
    Faz ingestão REAL de dados históricos a partir do football-data.co.uk (CSV)
    """

    if league_code not in LEAGUES:
        raise HTTPException(
            status_code=400,
            detail=f"Liga inválida. Use uma destas: {list(LEAGUES.keys())}",
        )

    league = LEAGUES[league_code]
    competition_id = league["competition_id"]

    csv_url = f"{FOOTBALL_DATA_BASE_URL}/{season}/{league_code}.csv"

    try:
        response = requests.get(csv_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao baixar CSV: {str(e)}",
        )

    csv_file = io.StringIO(response.text)
    reader = csv.DictReader(csv_file)

    inserted = 0

    for row in reader:
        try:
            # Evita duplicidade
            exists = (
                db.query(HistoricalMatches)
                .filter(
                    HistoricalMatches.home_team == row.get("HomeTeam"),
                    HistoricalMatches.away_team == row.get("AwayTeam"),
                    HistoricalMatches.season == int(season),
                    HistoricalMatches.competition_id == competition_id,
                )
                .first()
            )

            if exists:
                continue

            match = HistoricalMatches(
                competition_id=competition_id,
                season=int(season),
                home_team=row.get("HomeTeam"),
                away_team=row.get("AwayTeam"),
                home_goals_ft=int(row.get("FTHG", 0) or 0),
                away_goals_ft=int(row.get("FTAG", 0) or 0),
                home_goals_ht=int(row.get("HTHG", 0) or 0),
                away_goals_ht=int(row.get("HTAG", 0) or 0),
            )

            db.add(match)
            inserted += 1

        except Exception:
            # ignora linha quebrada sem derrubar ingestão
            continue

    db.commit()

    return {
        "league_code": league_code,
        "league_name": league["name"],
        "competition_id": competition_id,
        "season": season,
        "inserted": inserted,
        "source": csv_url,
    }
