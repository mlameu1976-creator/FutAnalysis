import os
import requests

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"


class APIFootballService:
    @staticmethod
    def _headers():
        return {"x-apisports-key": API_KEY}

    @staticmethod
    def get_matches(league=None, date=None, next_games=False):
        params = {}

        if league:
            params["league"] = league
            params["season"] = 2024

        if date:
            params["date"] = date

        if next_games:
            params["next"] = 20

        r = requests.get(
            f"{BASE_URL}/fixtures",
            headers=APIFootballService._headers(),
            params=params,
        )
        r.raise_for_status()
        return r.json()["response"]

    @staticmethod
    def get_odds_by_fixture(fixture_id: int):
        r = requests.get(
            f"{BASE_URL}/odds",
            headers=APIFootballService._headers(),
            params={"fixture": fixture_id},
        )
        r.raise_for_status()
        return r.json()["response"]
