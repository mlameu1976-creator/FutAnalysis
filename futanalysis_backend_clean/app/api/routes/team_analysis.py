from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.team_analysis_service import TeamAnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/last-games")
def analyze_last_games(
    team: str = Query(...),
    limit: int = Query(5)
):
    db: Session = SessionLocal()
    try:
        return TeamAnalysisService.last_games_analysis(db, team, limit)
    finally:
        db.close()
