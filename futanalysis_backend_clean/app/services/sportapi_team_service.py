import os
import requests
from dotenv import load_dotenv

load_dotenv()


class SportAPITeamService:
    def __init__(self):
        self.api_key = os.getenv("SPORTAPI_KEY")
        self.host = os.getenv("SPORTAPI_HOST")

        if not self.api_key or not self.host:
            raise RuntimeError("SPORTAPI_KEY ou SPORTAPI_HOST não configurados no .env")

        self.base_url = f"https://{self.host}/football"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host,
        }

    def get_teams_by_season(self, season_id: int):
        url = f"{self.base_url}/seasons/{season_id}/teams"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        # A SportAPI retorna tudo dentro de "response"
        return response.json().get("response", [])
