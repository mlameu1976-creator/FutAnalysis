from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.match import Match

router = APIRouter(prefix="/leagues", tags=["Leagues"])


@router.get("")
def list_leagues(db: Session = Depends(get_db)):

    leagues = (
        db.query(Match.league_id)
        .distinct()
        .order_by(Match.league_id)
        .all()
    )

    return [
        {
            "id": league.league_id
        }
        for league in leagues
    ]