import requests
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
import pytz  # ✅ CORREÇÃO AQUI

from app.models.match import Match
from app.models.league import League


API_KEY = "844189"
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"


def ingest_future_matches(db: Session):

    print("Buscando jogos futuros da API...")

    leagues = db.query(League).all()

    rows = []

    for league in leagues:

        if not league.external_id:
            continue

        url = f"{BASE_URL}/eventsnextleague.php?id={league.external_id}"

        try:
            response = requests.get(url, timeout=30)
            data = response.json()
        except Exception as e:
            print("Erro API:", e)
            continue

        events = data.get("events")

        if not events:
            continue

        for event in events:

            event_id = event.get("idEvent")

            if not event_id:
                continue

            date_str = event.get("dateEvent")
            time_str = event.get("strTime") or "00:00:00"

            if not date_str:
                continue

            try:
                # 🔥 UTC vindo da API
                utc_datetime = datetime.strptime(
                    f"{date_str} {time_str}",
                    "%Y-%m-%d %H:%M:%S"
                )

                # 🔥 CONVERSÃO PARA BRASIL
                utc = pytz.utc
                brasil = pytz.timezone("America/Sao_Paulo")

                utc_datetime = utc.localize(utc_datetime)
                match_date = utc_datetime.astimezone(brasil)

            except Exception as e:
                print("Erro ao converter data:", e)
                continue

            rows.append({
                "external_id": int(event_id),
                "league_id": league.id,
                "home_team": event.get("strHomeTeam"),
                "away_team": event.get("strAwayTeam"),
                "match_date": match_date,
                "season": event.get("strSeason"),
                "home_goals": None,
                "away_goals": None,
                "is_finished": False,
            })

    if not rows:
        print("Nenhum jogo retornado pela API")
        return 0

    stmt = insert(Match).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["external_id"])

    db.execute(stmt)
    db.commit()

    print("Jogos processados:", len(rows))

    return len(rows)