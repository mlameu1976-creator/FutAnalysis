import requests
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.match import Match
from app.models.league import League


API_KEY = "844189"
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"


def ensure_league_exists(db: Session, league_id: int):

    league = db.query(League).filter(League.id == league_id).first()

    if league:
        return

    try:
        new_league = League(
            id=league_id,
            name=f"League {league_id}",  # placeholder seguro
            country="Unknown"
        )

        db.add(new_league)
        db.commit()

        print(f"🆕 Liga criada automaticamente: {league_id}")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar liga {league_id}: {e}")


def ingest_historical_matches(db: Session, league_id: int, season: str):

    # 🔥 GARANTE INTEGRIDADE REFERENCIAL
    ensure_league_exists(db, league_id)

    url = f"{BASE_URL}/eventsseason.php?id={league_id}&s={season}"

    try:
        response = requests.get(url, timeout=30)
        data = response.json()
    except Exception as e:
        print("Erro API:", e)
        return 0

    events = data.get("events")

    if not events or not isinstance(events, list):
        print(f"⚠️ Nenhum evento válido para liga {league_id} temporada {season}")
        return 0

    inserted = 0
    errors = 0

    for event in events:

        if not isinstance(event, dict):
            continue

        try:
            event_id = event.get("idEvent")

            if not event_id:
                continue

            date_str = event.get("dateEvent")
            time_str = event.get("strTime") or "00:00:00"

            if not date_str:
                continue

            match_date = datetime.strptime(
                f"{date_str} {time_str}",
                "%Y-%m-%d %H:%M:%S"
            )

            home_goals = event.get("intHomeScore")
            away_goals = event.get("intAwayScore")

            if home_goals is None:
                home_goals = 0
            if away_goals is None:
                away_goals = 0

            home_goals = int(home_goals)
            away_goals = int(away_goals)

            row = {
                "external_id": int(event_id),
                "league_id": league_id,
                "home_team": event.get("strHomeTeam"),
                "away_team": event.get("strAwayTeam"),
                "match_date": match_date,
                "season": season,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "is_finished": True,
            }

            stmt = insert(Match).values(**row)
            stmt = stmt.on_conflict_do_nothing(index_elements=["external_id"])

            try:
                db.execute(stmt)
                db.commit()
                inserted += 1

            except Exception as e:
                db.rollback()
                errors += 1
                print(f"❌ Erro jogo ID {event_id}: {e}")
                continue

        except Exception as e:
            errors += 1
            print(f"❌ Erro parsing jogo: {e}")
            continue

    print(f"✔ Inseridos: {inserted} | ❌ Erros: {errors}")

    return inserted