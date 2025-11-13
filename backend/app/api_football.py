import os
import httpx
API_KEY = os.getenv('API_FOOTBALL_KEY')
BASE = 'https://v3.football.api-sports.io'
HEADERS = {'x-apisports-key': API_KEY} if API_KEY else {}
async def fetch_fixtures(league_id=None, season=None):
    if not API_KEY:
        raise RuntimeError('API_FOOTBALL_KEY not set in env')
    url = f"{BASE}/fixtures"
    params = {}
    if league_id: params['league'] = league_id
    if season: params['season'] = season
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, headers=HEADERS, timeout=20.0)
        r.raise_for_status()
        return r.json()
