from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta

from app.database import get_db
from app.models.match import Match
from app.models.opportunity import Opportunity
from app.models.league import League


router = APIRouter()


@router.get("/opportunities")
def get_opportunities(
    date: str = Query("all"),
    limit: int = Query(500),
    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Opportunity.id,
            Match.home_team,
            Match.away_team,
            Match.match_date,
            League.name.label("league"),
            Opportunity.market,
            Opportunity.probability,
        )
        .join(Match, Opportunity.match_id == Match.id)

        # 🔥 JOIN CORRETO (external_id)
        .join(League, Match.league_id == League.external_id)

        # impedir jogos antigos
        .filter(func.date(Match.match_date) >= func.current_date())
    )

    # -----------------------------
    # FILTRO DE DATA
    # -----------------------------

    if date == "today":
        query = query.filter(
            func.date(Match.match_date) == func.current_date()
        )

    elif date == "tomorrow":
        query = query.filter(
            func.date(Match.match_date) == func.current_date() + 1
        )

    # ordenação
    query = query.order_by(Match.match_date.asc())

    # limite (performance)
    query = query.limit(limit)

    results = query.all()

    return [
        {
            "id": row.id,
            "home_team": row.home_team,
            "away_team": row.away_team,
            "match_date": row.match_date - timedelta(hours=3),
            "league": row.league,
            "market": row.market,
            "probability": row.probability,
        }
        for row in results
    ]