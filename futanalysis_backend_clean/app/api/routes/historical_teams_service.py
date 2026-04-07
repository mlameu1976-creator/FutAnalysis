# app/routes/historical_teams.py

from fastapi import APIRouter
from app.services.historical_teams_service import HistoricalTeamsService

router = APIRouter(
    prefix="/historical",
    tags=["Historical"]
)


@router.get("/teams")
def list_historical_teams():
    teams = HistoricalTeamsService.list_teams()
    return teams
