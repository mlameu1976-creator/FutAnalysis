from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.match_ingestion_service import ingest_matches

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"]
)


@router.post("/matches")
def ingest_historical_matches(
    competition_id: int = Query(...),
    season: int = Query(...),
    limit: int = Query(20),
    db: Session = Depends(get_db),
):
    return ingest_matches(
        db=db,
        competition_id=competition_id,
        season=season,
        limit=limit,
    )
