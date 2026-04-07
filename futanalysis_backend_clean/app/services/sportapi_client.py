import os
import requests

class SportApiClient:
    def __init__(self):
        self.key = os.getenv("SPORTAPI_KEY")
        if not self.key:
            raise RuntimeError("SPORTAPI_KEY não configurada no .env")

        self.base_url = "https://sportapi7.p.rapidapi.com/api/v1"
        self.headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"
        }

    def normalize(self, name: str):
        return name.split(" ")[0]  # Bologna FC → Bologna

    def get_last_matches(self, team_name: str, limit: int = 5):
        team = self.normalize(team_name)

        r = requests.get(
            f"{self.base_url}/search/{team}",
            headers=self.headers,
            timeout=10
        )

        if r.status_code != 200:
            return None

        # MOCK CONTROLADO enquanto evoluímos
        return [
            {"goals_for": 2},
            {"goals_for": 1},
            {"goals_for": 3},
            {"goals_for": 0},
            {"goals_for": 2},
        ]
