import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()


class SportAPIHistoryService:
    def __init__(self):
        # 🔥 USANDO O MESMO PADRÃO DO RESTO DO PROJETO
        self.api_key = os.getenv("SPORTAPI_KEY")
        self.host = os.getenv("SPORTAPI_HOST")

        if not self.api_key:
            raise RuntimeError("SPORTAPI_KEY não configurada no .env")

        if not self.host:
            raise RuntimeError("SPORTAPI_HOST não configurada no .env")

        self.base_url = f"https://{self.host}"

        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }

    def get_last_matches(self, team_id: int, limit: int = 10):
        url = f"{self.base_url}/fixtures"
        params = {
            "team": team_id,
            "last": limit
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 429:
            print("⏳ Rate limit atingido, aguardando...")
            time.sleep(1)
            response = requests.get(url, headers=self.headers, params=params)

        response.raise_for_status()
        return response.json().get("response", [])
