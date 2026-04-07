import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()


class FootballDataHistoryService:
    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_API_KEY")
        if not self.api_key:
            raise RuntimeError("FOOTBALL_DATA_API_KEY não configurada no .env")

        self.base_url = "https://api.football-data.org/v4"
        self.headers = {
            "X-Auth-Token": self.api_key
        }

    def _safe_request(self, url, params=None):
        """
        Request seguro:
        - respeita rate limit
        - NÃO quebra o sync
        """
        try:
            res = requests.get(url, headers=self.headers, params=params)

            if res.status_code == 429:
                print("⏳ Rate limit atingido. Aguardando 15s...")
                time.sleep(15)
                return None

            res.raise_for_status()
            return res.json()

        except Exception as e:
            print("❌ Erro na API:", e)
            return None

    def get_last_matches(self, team_id: int, limit: int = 10):
        url = f"{self.base_url}/teams/{team_id}/matches"
        params = {
            "limit": limit,
            "status": "FINISHED"
        }

        data = self._safe_request(url, params=params)
        if not data:
            return []

        return data.get("matches", [])

    def get_teams_by_league(self, league_code: str):
        url = f"{self.base_url}/competitions/{league_code}/teams"
        data = self._safe_request(url)

        if not data:
            return []

        return data.get("teams", [])
