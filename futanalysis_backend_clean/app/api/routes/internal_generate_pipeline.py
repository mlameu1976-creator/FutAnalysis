from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.pipeline.generate_pre_match_features import generate_pre_match_features
from app.services.opportunity_engine import run_opportunity_engine

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/internal/generate-pipeline")
def generate_pipeline(db: Session = Depends(get_db)):

    generate_pre_match_features(db)
    run_opportunity_engine(db)

    return {"status": "pipeline executado"}
