import requests
from sqlalchemy.orm import Session

from app.models.match import Match


API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsseason.php"


def ingest_league_season(db: Session, league_id: int, season: str):

    try:

        response = requests.get(
            API_URL,
            params={"id": league_id, "s": season},
            timeout=30
        )

        if response.status_code != 200:
            return

        try:
            data = response.json()
        except Exception:
            return

        events = data.get("events")

        if not events:
            return

        inserted = 0
        ignored = 0

        for event in events:

            external_id = event.get("idEvent")

            if not external_id:
                continue

            exists = db.query(Match).filter(
                Match.external_id == external_id
            ).first()

            if exists:
                ignored += 1
                continue

            match = Match(
                external_id=external_id,
                league_id=league_id,
                home_team=event.get("strHomeTeam"),
                away_team=event.get("strAwayTeam"),
                match_date=event.get("dateEvent"),
                season=season,
                home_goals=event.get("intHomeScore"),
                away_goals=event.get("intAwayScore"),
                is_finished=True
            )

            db.add(match)

            inserted += 1

        db.commit()

        if inserted > 0:
            print(f"Jogos históricos inseridos: {inserted}")

    except Exception as e:

        print(f"Erro ao baixar temporada {season}: {e}")
