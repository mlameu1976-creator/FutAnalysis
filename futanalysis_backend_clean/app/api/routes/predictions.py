from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.match import Match
from app.models.opportunity import Opportunity
from app.models.league import League

router = APIRouter()


@router.get("/predictions")
def get_predictions(
    date: str = Query("today"),
    league: str | None = None,
    market: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
):

    query = (
        db.query(
            Opportunity.id,

            Match.home_team.label("home"),
            Match.away_team.label("away"),
            Match.match_date.label("date"),

            League.name.label("league"),

            Opportunity.market,
            Opportunity.probability,
        )
        .join(Match, Opportunity.match_id == Match.id)

        # 🔥 JOIN CORRETO
        .join(League, Match.league_id == League.external_id)
    )

    # -----------------------------
    # DATA
    # -----------------------------
    if date == "today":
        query = query.filter(func.date(Match.match_date) == func.current_date())

    elif date == "tomorrow":
        query = query.filter(func.date(Match.match_date) == func.current_date() + 1)

    else:
        query = query.filter(func.date(Match.match_date) >= func.current_date())

    # -----------------------------
    # FILTROS
    # -----------------------------
    if league:
        query = query.filter(League.name == league)

    if market:
        query = query.filter(Opportunity.market == market)

    query = query.order_by(Opportunity.probability.desc()).limit(limit)

    results = query.all()

    return [
        {
            "id": r.id,
            "home": r.home,
            "away": r.away,
            "date": r.date,
            "league": r.league,
            "market": r.market,
            "probability": r.probability,
        }
        for r in results
    ]