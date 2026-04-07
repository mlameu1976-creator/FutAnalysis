import os
import requests
from datetime import date, timedelta


class ApiFootballClient:
    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(self):
        self.api_key = os.getenv("API_FOOTBALL_KEY")
        if not self.api_key:
            raise RuntimeError("API_FOOTBALL_KEY não configurada no .env")

        self.headers = {
            "x-apisports-key": self.api_key
        }

    # 🔹 Jogos FUTUROS (HOJE e AMANHÃ)
    def get_fixtures_today_tomorrow(self, league_id: int, season: int):
        today = date.today()
        tomorrow = today + timedelta(days=1)

        url = f"{self.BASE_URL}/fixtures"
        params = {
            "league": league_id,
            "season": season,
            "from": today.isoformat(),
            "to": tomorrow.isoformat(),
            "status": "NS"  # Not Started (futuros)
        }

        response = requests.get(url, headers=self.headers, params=params, timeout=15)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro API-Football fixtures: {response.status_code} - {response.text}"
            )

        return response.json().get("response", [])

    # 🔹 Últimos N jogos de um time (FINALIZADOS)
    def get_last_games(self, team_id: int, limit: int = 5):
        url = f"{self.BASE_URL}/fixtures"
        params = {
            "team": team_id,
            "last": limit,
            "status": "FT"
        }

        response = requests.get(url, headers=self.headers, params=params, timeout=15)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro API-Football last games: {response.status_code} - {response.text}"
            )

        return response.json().get("response", [])
