import os
import sys
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import SessionLocal
from app.models import Team
from app.models import TeamAlias
from app.services.name_normalizer import normalize_name


def rebuild_aliases():
    db: Session = SessionLocal()

    # limpa aliases antigos (se houver)
    db.query(TeamAlias).delete()
    db.commit()

    teams = db.query(Team).all()
    created = 0

    for team in teams:
        alias_value = normalize_name(team.name)

        alias = TeamAlias(
            team_id=team.id,
            alias=alias_value
        )
        db.add(alias)
        created += 1

    db.commit()
    db.close()

    print(f"✅ Aliases recriados: {created}")


if __name__ == "__main__":
    rebuild_aliases()
