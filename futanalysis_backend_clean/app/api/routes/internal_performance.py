from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.performance_service import calculate_performance

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/performance")
def get_performance(db: Session = Depends(get_db)):
    return calculate_performance(db)