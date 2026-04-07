from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.database import get_db
from app.models.opportunity import Opportunity
from app.models.match import Match
from app.models.league import League

router = APIRouter()


@router.get("/predictions")
def get_predictions(
    day: str = Query("today"),
    db: Session = Depends(get_db)
):

    today = date.today()
    tomorrow = today + timedelta(days=1)
    after_tomorrow = today + timedelta(days=2)

    query = (
        db.query(
            Opportunity.market,
            Opportunity.probability,
            Match.match_date,
            Match.home_team,
            Match.away_team,
            League.name.label("league_name"),
        )
        .join(Match, Opportunity.match_id == Match.id)
        .join(League, Match.league_id == League.id)
    )

    if day == "today":
        query = query.filter(func.date(Match.match_date) == today)

    elif day == "tomorrow":
        query = query.filter(func.date(Match.match_date) == tomorrow)

    elif day == "all":
        query = query.filter(func.date(Match.match_date) >= today)

    rows = (
        query
        .order_by(Opportunity.probability.desc())
        .limit(50)
        .all()
    )

    result = []

    for r in rows:
        result.append({
            "date": r.match_date,
            "league": r.league_name,
            "home": r.home_team,
            "away": r.away_team,
            "market": r.market,
            "probability": r.probability
        })

    return result