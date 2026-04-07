from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.match import Match

router = APIRouter()


@router.get("/rankings")
def get_rankings(db: Session = Depends(get_db)):
    """
    Ranking simples baseado nos jogos armazenados.
    Evita dependência de models ou imports quebrados.
    """

    teams = (
        db.query(Match.home_team)
        .distinct()
        .all()
    )

    return [
        {
            "team": team_name
        }
        for (team_name,) in teams
        if team_name
    ]