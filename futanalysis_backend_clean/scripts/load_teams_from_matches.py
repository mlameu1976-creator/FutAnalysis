import os
import sys
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import SessionLocal
from app.models import HistoricalMatch
from app.models import Team


def load_teams():
    db: Session = SessionLocal()

    matches = db.query(HistoricalMatches).all()
    print(f"🔍 Partidas encontradas: {len(matches)}")

    names = set()
    for m in matches:
        if m.home_team:
            names.add(m.home_team)
        if m.away_team:
            names.add(m.away_team)

    created = 0
    for name in names:
        exists = db.query(Team).filter(Team.name == name).first()
        if exists:
            continue

        db.add(Team(name=name, short_name=name))
        created += 1

    db.commit()
    db.close()

    print(f"✅ Times criados: {created}")


if __name__ == "__main__":
    load_teams()
