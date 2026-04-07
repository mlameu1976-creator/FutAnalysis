from sqlalchemy.orm import Session
from app.models import Team
from app.models import TeamAlias

def resolve_team_id(db: Session, name: str) -> int | None:
    alias = (
        db.query(TeamAlias)
        .filter(TeamAlias.alias == name.strip().lower())
        .first()
    )
    return alias.team_id if alias else None
