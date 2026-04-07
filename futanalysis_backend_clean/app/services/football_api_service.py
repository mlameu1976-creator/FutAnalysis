import os
import requests
from datetime import date, timedelta
from app.models.match import Match


API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io/fixtures"


def fetch_matches_for_date(target_date):
    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": target_date.isoformat()
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print("Erro API:", response.text)
        return []

    data = response.json()

    return data.get("response", [])


def sync_matches(db):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    total_created = 0

    for target_date in [today, tomorrow]:
        fixtures = fetch_matches_for_date(target_date)

        for fixture in fixtures:
            fixture_id = str(fixture["fixture"]["id"])

            existing = db.query(Match).filter(
                Match.external_id == fixture_id
            ).first()

            if existing:
                continue

            new_match = Match(
                external_id=fixture_id,
                league_name=fixture["league"]["name"],
                status=fixture["fixture"]["status"]["short"],
                home_team=fixture["teams"]["home"]["name"],
                away_team=fixture["teams"]["away"]["name"],
                match_date=target_date,
                is_finished=fixture["fixture"]["status"]["short"] == "FT",
            )

            db.add(new_match)
            total_created += 1

    db.commit()
    return total_created