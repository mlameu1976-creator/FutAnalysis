import os
from dotenv import load_dotenv

load_dotenv()

SPORTSDB_API_KEY = os.getenv("SPORTSDB_API_KEY")

SPORTSDB_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{SPORTSDB_API_KEY}"
