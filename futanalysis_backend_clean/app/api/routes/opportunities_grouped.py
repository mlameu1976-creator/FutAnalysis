from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from app.database import get_db
from app.models.opportunity import Opportunity
from app.models.match import Match

router = APIRouter(prefix="/opportunities/grouped", tags=["Public Opportunities"])


@router.get("")
def list_grouped_opportunities(
    season: Optional[str] = Query(None),
    league_id: Optional[int] = Query(None),
    confidence_min: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Opportunity.match_id,
            Opportunity.match_label,
            Opportunity.market,
            Opportunity.score,
            Opportunity.confidence,
            Match.match_date,
            Match.home_team,
            Match.away_team,
        )
        .join(Match, Match.id == Opportunity.match_id)
    )

    # ===== FILTROS =====
    if season:
        query = query.filter(Match.season == season)

    if league_id:
        query = query.filter(Match.league_id == league_id)

    if confidence_min:
        query = query.filter(Opportunity.confidence >= confidence_min)

    query = query.order_by(desc(Opportunity.confidence))

    results = query.all()

    # ===== AGRUPAMENTO EM MEMÓRIA =====
    grouped = {}

    for r in results:
        if r.match_id not in grouped:
            grouped[r.match_id] = {
                "match_id": r.match_id,
                "match_label": r.match_label,
                "match_date": r.match_date,
                "home_team": r.home_team,
                "away_team": r.away_team,
                "markets": []
            }

        grouped[r.match_id]["markets"].append({
            "market": r.market,
            "score": r.score,
            "confidence": r.confidence
        })

    matches_list = list(grouped.values())

    # ===== PAGINAÇÃO POR JOGO =====
    total = len(matches_list)
    offset = (page - 1) * limit
    paginated = matches_list[offset: offset + limit]

    return {
        "page": page,
        "limit": limit,
        "total_matches": total,
        "total_pages": (total + limit - 1) // limit,
        "data": paginated
    }