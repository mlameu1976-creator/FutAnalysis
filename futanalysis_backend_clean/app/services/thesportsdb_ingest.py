import os
import requests
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.match import Match

# ===============================
# CONFIGURAÇÃO
# ===============================

API_KEY = os.getenv("THESPORTSDB_API_KEY")
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# Exemplo: Premier League = 4328
LEAGUE_IDS = [
    4328,  # Premier League
    4331,  # Bundesliga
    4332,  # Serie A
    4334,  # La Liga
]

# ===============================
# HELPERS
# ===============================

def get_teams_by_league(league_id):
    url = f"{BASE_URL}/lookup_all_teams.php?id={league_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("teams") or []


def get_future_events_for_team(team_id):
    url = f"{BASE_URL}/eventsnext.php?id={team_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("events") or []


def parse_event(event):
    if not event.get("dateEvent"):
        return None

    match_date = datetime.strptime(event["dateEvent"], "%Y-%m-%d").date()

    # 🔒 filtro definitivo: SOMENTE jogos futuros
    if match_date < date.today():
        return None

    return {
        "external_id": event["idEvent"],
        "home_team": event.get("strHomeTeam"),
        "away_team": event.get("strAwayTeam"),
        "league": event.get("strLeague"),
        "match_date": match_date,
        "is_finished": False,
    }


# ===============================
# INGESTÃO PRINCIPAL
# ===============================

def ingest_future_matches():
    db: Session = SessionLocal()
    inserted = 0
    skipped = 0
    seen_events = set()

    try:
        for league_id in LEAGUE_IDS:
            teams = get_teams_by_league(league_id)

            for team in teams:
                team_id = team["idTeam"]
                events = get_future_events_for_team(team_id)

                for event in events:
                    parsed = parse_event(event)
                    if not parsed:
                        continue

                    # evita duplicação (mesmo jogo vem por 2 times)
                    if parsed["external_id"] in seen_events:
                        continue

                    seen_events.add(parsed["external_id"])

                    exists = (
                        db.query(Match)
                        .filter(Match.external_id == parsed["external_id"])
                        .first()
                    )

                    if exists:
                        skipped += 1
                        continue

                    match = Match(**parsed)
                    db.add(match)
                    inserted += 1

        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    print(f"Ingestão finalizada | Inseridos: {inserted} | Ignorados: {skipped}")


if __name__ == "__main__":
    ingest_future_matches()