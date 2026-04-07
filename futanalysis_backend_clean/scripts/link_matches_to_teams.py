import os
import sys
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import SessionLocal
from app.models import HistoricalMatch
from app.models import TeamAlias
from app.services.name_normalizer import normalize_name


def link_matches():
    db: Session = SessionLocal()

    aliases = {
        normalize_name(a.alias): a.team_id
        for a in db.query(TeamAlias).all()
    }

    matches = db.query(HistoricalMatches).all()
    updated = 0

    for m in matches:
        if m.home_team_id and m.away_team_id:
            continue

        home_norm = normalize_name(m.home_team)
        away_norm = normalize_name(m.away_team)

        if home_norm in aliases:
            m.home_team_id = aliases[home_norm]
        if away_norm in aliases:
            m.away_team_id = aliases[away_norm]

        if m.home_team_id or m.away_team_id:
            updated += 1

    db.commit()
    db.close()

    print(f"✅ Jogos atualizados com team_id: {updated}")


if __name__ == "__main__":
    link_matches()
