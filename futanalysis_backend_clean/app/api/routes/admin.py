from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.team_stats_service import TeamStatsService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/update-team-stats")
async def update_team_stats(db: Session = Depends(get_db)):
    service = TeamStatsService()
    await service.update_from_recent_matches(db)
    return {"status": "ok"}
