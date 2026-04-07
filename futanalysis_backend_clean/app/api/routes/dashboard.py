from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.match import Match
from app.models.pre_match_features import PreMatchFeatures
from app.models.opportunity import Opportunity

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/matches/future")
def get_future_matches(db: Session = Depends(get_db)):
    return (
        db.query(Match)
        .filter(Match.is_finished.is_(False))
        .order_by(Match.match_date.asc())
        .limit(50)
        .all()
    )


@router.get("/features")
def get_pre_match_features(db: Session = Depends(get_db)):
    return db.query(PreMatchFeatures).limit(50).all()


@router.get("/opportunities")
def get_opportunities(db: Session = Depends(get_db)):
    return (
        db.query(Opportunity)
        .order_by(Opportunity.score.desc())
        .limit(50)
        .all()
    )