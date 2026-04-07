from datetime import datetime
import requests

from sqlalchemy.orm import Session

from app.models.match import Match


API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php"


def sync_matches(db: Session):

    today = datetime.utcnow().strftime("%Y-%m-%d")

    url = f"{API_URL}?d={today}&s=Soccer"

    response = requests.get(url)

    data = response.json()

    events = data.get("events", [])

    created = 0

    for event in events:

        event_id = event.get("idEvent")

        if not event_id:
            continue

        exists = db.query(Match).filter(Match.external_id == event_id).first()

        if exists:
            continue

        date_event = event.get("dateEvent")
        time_event = event.get("strTime")

        # 🔥 juntar data + hora
        match_datetime = None

        if date_event and time_event:

            try:

                match_datetime = datetime.strptime(
                    f"{date_event} {time_event}",
                    "%Y-%m-%d %H:%M:%S"
                )

            except:

                match_datetime = datetime.strptime(
                    date_event,
                    "%Y-%m-%d"
                )

        match = Match(

            external_id=event_id,

            league_id=event.get("idLeague"),

            season=event.get("strSeason"),

            home_team=event.get("strHomeTeam"),

            away_team=event.get("strAwayTeam"),

            match_date=match_datetime,

            is_finished=False

        )

        db.add(match)

        created += 1

    db.commit()

    return created