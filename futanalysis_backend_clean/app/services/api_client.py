import requests
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def fetch_fixtures_by_date(date_str: str):
    url = f"{BASE_URL}/fixtures?date={date_str}"
    res = requests.get(url, headers=HEADERS, timeout=30)
    data = res.json()
    return data.get("response", [])

def fetch_live_fixtures():
    url = f"{BASE_URL}/fixtures?live=all"
    res = requests.get(url, headers=HEADERS, timeout=30)
    data = res.json()
    return data.get("response", [])
