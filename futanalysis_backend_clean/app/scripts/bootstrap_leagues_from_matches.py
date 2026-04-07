import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.match import Match
from app.models.league import League


def run():
    db: Session = SessionLocal()

    try:
        matches = db.query(Match).all()

        if not matches:
            print("No matches found.")
            return

        created = 0

        for m in matches:
            # aqui usamos os dados que já EXISTEM nos matches
            league = (
                db.query(League)
                .filter(
                    League.external_id == str(m.league_id),
                    League.season == m.season
                )
                .first()
            )

            if league:
                continue

            league = League(
                external_id=str(m.league_id),
                name=getattr(m, "league_name", f"League {m.league_id}"),
                country="UNKNOWN",
                season=m.season,
            )

            db.add(league)
            db.commit()

            # agora conectamos os matches a essa league real
            db.query(Match).filter(
                Match.league_id == m.league_id,
                Match.season == m.season
            ).update(
                {"league_id": league.id}
            )
            db.commit()

            created += 1

        print(f"Leagues created: {created}")

    finally:
        db.close()


if __name__ == "__main__":
    run()