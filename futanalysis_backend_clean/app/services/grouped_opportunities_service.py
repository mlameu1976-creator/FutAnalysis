from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.match import Match
from app.models.opportunity import Opportunity


def build_grouped_opportunities(db: Session):

    results = (
        db.query(
            Match.id.label("match_id"),
            Match.home_team,
            Match.away_team,
            Match.match_date,
            func.count(Opportunity.id).label("total_markets"),
        )
        .join(Opportunity, Opportunity.match_id == Match.id)
        .group_by(
            Match.id,
            Match.home_team,
            Match.away_team,
            Match.match_date,
        )
        .order_by(Match.match_date)
        .all()
    )

    grouped = []

    for row in results:
        grouped.append(
            {
                "match_id": row.match_id,
                "home_team": row.home_team,
                "away_team": row.away_team,
                "match_date": row.match_date,
                "total_markets": row.total_markets,
            }
        )

    return grouped