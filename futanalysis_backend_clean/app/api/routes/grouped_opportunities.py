from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.grouped_opportunities_service import build_grouped_opportunities

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


@router.get("/grouped")
def grouped_opportunities(db: Session = Depends(get_db)):
    return build_grouped_opportunities(db)
