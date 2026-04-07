import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.match import Match

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("THESPORTSDB_API_KEY")
BASE_URL = "https://www.thesportsdb.com/api/v1/json"

# Ligas principais
LEAGUES = {
    4328: "Premier League",
    4335: "La Liga",
    4332: "Serie A",
    4331: "Bundesliga",
    4334: "Ligue 1",
}


# =========================
# API CALL
# =========================
def get_next_events_by_league(league_id: int):
    url = f"{BASE_URL}/{API_KEY}/eventsnextleague.php"
    params = {"id": league_id}

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()

    data = r.json()
    return data.get("events") or []


# =========================
# INGEST
# =========================
def ingest_future_matches():
    db: Session = SessionLocal()

    inserted = 0
    skipped = 0

    try:
        for league_id, league_name in LEAGUES.items():
            print(f"\n▶ Buscando próximos jogos: {league_name}")

            events = get_next_events_by_league(league_id)

            if not events:
                print("  ⚠ Nenhum evento retornado")
                continue

            for e in events:

                if not e.get("dateEvent"):
                    continue

                date_str = e.get("dateEvent")
                time_str = e.get("strTime")

                # =========================
                # CONVERTE DATA + HORÁRIO
                # =========================
                match_datetime = None

                try:
                    if time_str:
                        match_datetime = datetime.strptime(
                            f"{date_str} {time_str}",
                            "%Y-%m-%d %H:%M:%S"
                        )
                    else:
                        match_datetime = datetime.strptime(
                            date_str,
                            "%Y-%m-%d"
                        )
                except:
                    continue

                # Evita inserir jogos passados
                if match_datetime.date() < datetime.utcnow().date():
                    continue

                external_id = e.get("idEvent")

                exists = (
                    db.query(Match)
                    .filter(Match.external_id == external_id)
                    .first()
                )

                if exists:
                    skipped += 1
                    continue

                match = Match(
                    external_id=external_id,
                    league_id=league_id,
                    season=str(datetime.utcnow().year),
                    home_team=e.get("strHomeTeam"),
                    away_team=e.get("strAwayTeam"),
                    match_date=match_datetime,
                    status="NS",
                    is_finished=False,
                )

                db.add(match)
                inserted += 1

            db.commit()
            print(f"  ✔ Inseridos até agora: {inserted}")

        print("\n✅ INGESTÃO FINALIZADA")
        print(f"   Inseridos: {inserted}")
        print(f"   Ignorados: {skipped}")

    except Exception as ex:
        db.rollback()
        raise ex

    finally:
        db.close()


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    ingest_future_matches()