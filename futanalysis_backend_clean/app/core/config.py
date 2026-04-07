from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    API_FOOTBALL_KEY: str = os.getenv("API_FOOTBALL_KEY")
    FOOTBALL_DATA_API_KEY: str = os.getenv("FOOTBALL_DATA_API_KEY")

    def validate(self):
        if not self.API_FOOTBALL_KEY:
            raise RuntimeError("API_FOOTBALL_KEY não configurada no .env")
        if not self.FOOTBALL_DATA_API_KEY:
            raise RuntimeError("FOOTBALL_DATA_API_KEY não configurada no .env")

settings = Settings()
settings.validate()
