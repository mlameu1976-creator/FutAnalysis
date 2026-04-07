import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# 🔑 garante carregamento do .env SEM depender do uvicorn
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class FootballDataClient:
    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_API_KEY")

    def _headers(self):
        if not self.api_key:
            raise RuntimeError("FOOTBALL_DATA_API_KEY não configurada no .env")

        return {
            "X-Auth-Token": self.api_key
        }

    def get(self, endpoint: str, params: dict | None = None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
