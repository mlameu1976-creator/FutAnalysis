from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.opportunities_full_service import build_full_opportunities

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


@router.get("/full")
def get_full_opportunities(
    date: str | None = Query(None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    return build_full_opportunities(db, date)
