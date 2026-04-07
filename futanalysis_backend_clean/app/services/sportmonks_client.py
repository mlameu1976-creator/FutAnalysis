import os
import requests

class SportMonksClient:
    BASE_URL = "https://api.sportmonks.com/v3/football"

    def __init__(self):
        self.token = os.getenv("SPORTMONKS_API_TOKEN")
        if not self.token:
            raise RuntimeError("SPORTMONKS_API_TOKEN não encontrado no ambiente")

    def get(self, endpoint: str, params: dict | None = None):
        url = f"{self.BASE_URL}/{endpoint}"

        params = params or {}
        params["api_token"] = self.token

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro SportMonks [{response.status_code}]: {response.text}"
            )

        return response.json()
