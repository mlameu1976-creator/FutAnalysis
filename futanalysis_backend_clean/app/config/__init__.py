import os
from dotenv import load_dotenv
from pathlib import Path

# localizar o .env na raiz do backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(env_path)

SPORTSDB_API_KEY = os.getenv("SPORTSDB_API_KEY")

if not SPORTSDB_API_KEY:
    raise ValueError("SPORTSDB_API_KEY não definida no .env")

SPORTSDB_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{SPORTSDB_API_KEY}"