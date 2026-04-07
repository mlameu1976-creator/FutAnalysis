from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.opportunity_engine import OpportunityEngine

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/generate-opportunities")
def generate_opportunities(
    league_id: int,
    season: str,
    db: Session = Depends(get_db),
):
    """
    Gera oportunidades para uma liga e temporada específicas
    usando o OpportunityEngine já existente.
    """

    OpportunityEngine.run_for_league(
        db=db,
        league_id=league_id,
        season=season,
    )

    return {
        "status": "ok",
        "league_id": league_id,
        "season": season,
    }