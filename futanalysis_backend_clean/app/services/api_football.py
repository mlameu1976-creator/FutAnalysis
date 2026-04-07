import requests
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.cache import cache


class APIFootballService:
    BASE_URL = "https://v3.football.api-sports.io"

    HEADERS = {
        "x-apisports-key": settings.API_FOOTBALL_KEY
    }

    MIN_FREE_SEASON = 2022
    MAX_FREE_SEASON = 2024

    CACHE_TTL = 60 * 5  # 5 minutos

    @staticmethod
    def _safe_season(season: int | None) -> int:
        if season is None:
            return APIFootballService.MAX_FREE_SEASON

        if season < APIFootballService.MIN_FREE_SEASON:
            return APIFootballService.MIN_FREE_SEASON

        if season > APIFootballService.MAX_FREE_SEASON:
            return APIFootballService.MAX_FREE_SEASON

        return season

    @classmethod
    def _get(cls, endpoint: str, params: dict):
        cache_key = f"{endpoint}:{sorted(params.items())}"
        cached = cache.get(cache_key)

        if cached is not None:
            return cached

        url = f"{cls.BASE_URL}{endpoint}"

        response = requests.get(
            url=url,
            headers=cls.HEADERS,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            raise Exception(
                f"API-Football error | Status: {response.status_code} | Body: {response.text}"
            )

        data = response.json()

        if data.get("errors"):
            raise Exception(f"API-Football returned errors: {data['errors']}")

        result = data.get("response", [])
        cache.set(cache_key, result, cls.CACHE_TTL)

        return result

    @classmethod
    def get_last_team_matches(
        cls,
        team_id: int,
        season: int | None = None,
        limit: int = 5
    ):
        season = cls._safe_season(season)

        matches = cls._get(
            "/fixtures",
            {
                "team": team_id,
                "season": season,
                "from": "2022-01-01",
                "to": "2024-12-31"
            }
        )

        matches.sort(
            key=lambda m: m["fixture"]["date"],
            reverse=True
        )

        return matches[:limit]
