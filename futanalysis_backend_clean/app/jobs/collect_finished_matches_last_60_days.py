print(">>> FUTANALYSIS — COLLECT FINISHED MATCHES (LAST 60 DAYS / SAFE) <<<")

import os
import time
import requests
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.match import Match


# ---------------- CONFIG ----------------

API_KEY = os.getenv("THESPORTSDB_API_KEY")
BASE_URL = "https://www.thesportsdb.com/api/v1/json"

DAYS_BACK = 60
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3
SLEEP_BETWEEN_DAYS = 1  # respeita a API


# ---------------- API ----------------

def get_events_by_date(day: date):
    url = f"{BASE_URL}/{API_KEY}/eventsday.php"
    params = {"d": day.strftime("%Y-%m-%d")}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return data.get("events") or []

        except requests.exceptions.RequestException as e:
            print(f"[WARN] {day} tentativa {attempt}/{MAX_RETRIES} falhou: {e}")
            time.sleep(3)

    print(f"[SKIP] {day} ignorado após {MAX_RETRIES} tentativas")
    return []


# ---------------- JOB ----------------

def run():
    db: Session = SessionLocal()

    try:
        today = date.today()
        start_date = today - timedelta(days=DAYS_BACK)

        total_saved = 0
        current_date = start_date

        while current_date < today:
            print(f"[DAY {current_date}] Coletando jogos finalizados")

            events = get_events_by_date(current_date)
            print(f"[DAY {current_date}] eventos recebidos: {len(events)}")

            for e in events:
                if e.get("strSport") != "Soccer":
                    continue

                if e.get("strStatus") != "Match Finished":
                    continue

                external_id = e.get("idEvent")
                if not external_id:
                    continue

                exists = (
                    db.query(Match)
                    .filter(Match.external_id == external_id)
                    .first()
                )
                if exists:
                    continue

                try:
                    home_goals = int(e.get("intHomeScore"))
                    away_goals = int(e.get("intAwayScore"))
                except Exception:
                    continue

                try:
                    home_ht = int(e.get("intHomeScoreHT") or 0)
                    away_ht = int(e.get("intAwayScoreHT") or 0)
                except Exception:
                    home_ht = 0
                    away_ht = 0

                total_goals = home_goals + away_goals

                match = Match(
                    external_id=external_id,
                    league_id=e.get("idLeague"),
                    league_name=e.get("strLeague"),
                    season=e.get("strSeason"),
                    match_date=current_date,
                    home_team=e.get("strHomeTeam"),
                    away_team=e.get("strAwayTeam"),
                    home_goals=home_goals,
                    away_goals=away_goals,
                    home_goals_ht=home_ht,
                    away_goals_ht=away_ht,
                    status="Finished",
                    is_finished=True,
                    is_draw=home_goals == away_goals,
                    home_win=home_goals > away_goals,
                    away_win=away_goals > home_goals,
                    btts=home_goals > 0 and away_goals > 0,
                    over_15=total_goals >= 2,
                    over_25=total_goals >= 3,
                )

                db.add(match)
                total_saved += 1

            db.commit()
            current_date += timedelta(days=1)
            time.sleep(SLEEP_BETWEEN_DAYS)

        print(f"\n[OK] Total de jogos FINALIZADOS salvos: {total_saved}")

    except Exception as e:
        db.rollback()
        print("[ERROR]", e)

    finally:
        db.close()


if __name__ == "__main__":
    run()