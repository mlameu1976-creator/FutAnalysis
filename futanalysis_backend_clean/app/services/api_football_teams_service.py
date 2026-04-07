import os
import json
import urllib.request

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io/teams"


def fetch_teams_by_league(league_id: int, season: int = 2024):
    """
    Busca times reais de uma liga (API-Football).
    Usa apenas biblioteca padrão do Python.
    """

    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY não configurada")

    url = f"{BASE_URL}?league={league_id}&season={season}"

    request = urllib.request.Request(
        url,
        headers={"x-apisports-key": API_KEY}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read())

    teams = []

    for item in data.get("response", []):
        team = item.get("team", {})
        teams.append({
            "id": team.get("id"),
            "name": team.get("name"),
            "logo": team.get("logo"),
            "country": team.get("country"),
        })

    return teams
