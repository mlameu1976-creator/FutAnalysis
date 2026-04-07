import os
import json
import urllib.request

API_KEY = os.getenv("API_FOOTBALL_KEY")

BASE_URL = "https://v3.football.api-sports.io/leagues"


def fetch_leagues():
    """
    🔹 Busca ligas reais na API-Football
    🔹 Usando apenas biblioteca padrão do Python
    🔹 Compatível com ambiente corporativo (sem pip)
    """

    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY não configurada")

    request = urllib.request.Request(
        BASE_URL,
        headers={
            "x-apisports-key": API_KEY
        }
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read()
        data = json.loads(body)

    leagues = []

    for item in data.get("response", []):
        league = item.get("league", {})
        country = item.get("country", {})

        leagues.append({
            "id": league.get("id"),
            "name": league.get("name"),
            "country": country.get("name"),
            "logo": league.get("logo"),
        })

    return leagues
