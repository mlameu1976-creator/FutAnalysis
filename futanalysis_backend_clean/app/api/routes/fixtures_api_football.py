from fastapi import APIRouter, Query, HTTPException
import os
import requests

router = APIRouter(
    prefix="/fixtures",
    tags=["Fixtures"]
)

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io/fixtures"


@router.get("/upcoming")
def get_upcoming_fixtures(
    competition_id: int = Query(..., description="ID da liga na API-Football"),
    season: int = Query(..., description="Temporada (ex: 2024)"),
    limit: int = Query(10, description="Máximo de jogos"),
):
    if not API_FOOTBALL_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_FOOTBALL_KEY não configurada"
        )

    headers = {
        "x-apisports-key": API_FOOTBALL_KEY
    }

    params = {
        "league": competition_id,
        "season": season,
        "next": limit
    }

    try:
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=20
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao consultar API-Football: {str(e)}"
        )

    data = response.json()
    fixtures = []

    for item in data.get("response", []):
        fixtures.append({
            "match_id": item["fixture"]["id"],
            "home_team": item["teams"]["home"]["name"],
            "away_team": item["teams"]["away"]["name"],
            "match_date": item["fixture"]["date"],
            "competition_id": competition_id,
            "season": season,
            "status": item["fixture"]["status"]["short"],
        })

    return fixtures
