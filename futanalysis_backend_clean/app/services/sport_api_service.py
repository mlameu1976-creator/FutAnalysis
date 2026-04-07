import os
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()


class SportAPIService:
    def __init__(self):
        self.api_key = os.getenv("SPORT_API_KEY")
        if not self.api_key:
            raise RuntimeError("SPORT_API_KEY não configurada no .env")

        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": self.api_key
        }

    # =====================
    # TIMES POR LIGA
    # =====================
    def get_teams_by_league(self, league_id: int, season: int):
        url = f"{self.base_url}/teams"
        params = {"league": league_id, "season": season}
        res = requests.get(url, headers=self.headers, params=params)
        res.raise_for_status()
        return res.json()["response"]

    # =====================
    # HISTÓRICO
    # =====================
    def get_last_matches(self, team_id: int, season: int, limit: int = 10):
        url = f"{self.base_url}/fixtures"
        params = {"team": team_id, "season": season, "last": limit}
        res = requests.get(url, headers=self.headers, params=params)
        res.raise_for_status()
        return res.json()["response"]

    # =====================
    # JOGOS FUTUROS (CORRETO)
    # =====================
    def get_upcoming_matches(self, league_id: int):
        today = date.today().isoformat()

        url = f"{self.base_url}/fixtures"
        params = {
            "league": league_id,
            "from": today,
            "status": "NS"
        }

        res = requests.get(url, headers=self.headers, params=params)
        res.raise_for_status()
        return res.json()["response"]
