from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.team_service import sync_teams

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/sync")
def sync_teams_route(db: Session = Depends(get_db)):
    inserted = sync_teams(db)
    return {"inserted": inserted}
