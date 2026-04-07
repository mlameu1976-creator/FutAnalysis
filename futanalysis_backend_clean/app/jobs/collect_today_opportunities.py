from datetime import date, datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.opportunity import Opportunity
from app.services.thesportsdb_service import TheSportsDBService


def parse_kickoff(event: dict) -> datetime | None:
    date_event = event.get("dateEvent")
    time_event = event.get("strTime")

    if not date_event:
        return None

    # Normalização do horário
    if not time_event:
        time_event = "00:00"
    else:
        # remove timezone se existir (ex: 20:00:00+00:00)
        time_event = time_event.split("+")[0]

    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(
                f"{date_event} {time_event}",
                f"%Y-%m-%d {fmt}"
            )
        except ValueError:
            continue

    return None


def collect_today_opportunities():
    db: Session = SessionLocal()

    try:
        api = TheSportsDBService()
        today = date.today()

        events = api.get_events_by_date(today)

        if not events:
            print("⚠️ Nenhum jogo encontrado para hoje.")
            return

        saved = 0

        for event in events:
            if event.get("strSport") != "Soccer":
                continue

            kickoff = parse_kickoff(event)
            if kickoff is None:
                continue

            home = event.get("strHomeTeam")
            away = event.get("strAwayTeam")

            if not home or not away:
                continue

            match_name = f"{home} x {away}"

            markets = [
                ("over_1.5", 70),
                ("over_2.5", 60),
                ("btts", 58),
                ("goal_ht", 52),
                ("home_win", 55),
                ("away_win", 55),
            ]

            for market, score in markets:
                db.add(
                    Opportunity(
                        match=match_name,
                        market=market,
                        confidence=score,
                        score=score,
                        source="real-engine",
                        kickoff=kickoff,
                    )
                )
                saved += 1

        db.commit()
        print(f"✅ {saved} oportunidades salvas com kickoff válido.")

    finally:
        db.close()


if __name__ == "__main__":
    collect_today_opportunities()