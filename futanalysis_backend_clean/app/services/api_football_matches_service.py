import os
import json
import urllib.request
from datetime import datetime

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io/fixtures"


def fetch_matches_real(league: int | None = None, season: int = 2024):
    """
    🔹 Busca jogos reais (fixtures) da API-Football
    🔹 Fonte oficial de dados do projeto
    """

    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY não configurada")

    url = f"{BASE_URL}?season={season}"

    if league:
        url += f"&league={league}"

    request = urllib.request.Request(
        url,
        headers={"x-apisports-key": API_KEY}
    )

    with urllib.request.urlopen(request, timeout=25) as response:
        data = json.loads(response.read())

    matches = []

    for item in data.get("response", []):
        fixture = item.get("fixture", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})

        matches.append({
            "id": fixture.get("id"),
            "date": fixture.get("date"),
            "status": fixture.get("status", {}).get("short"),
            "home_team": teams.get("home", {}).get("name"),
            "away_team": teams.get("away", {}).get("name"),
            "home_goals": goals.get("home"),
            "away_goals": goals.get("away"),
            "league": item.get("league", {}).get("id"),
        })

    return matches
