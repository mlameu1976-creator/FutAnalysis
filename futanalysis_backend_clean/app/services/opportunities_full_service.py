from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Match
from app.models import MatchAnalysis


def build_full_opportunities(db: Session, date: str | None = None):
    query = (
        db.query(Match, MatchAnalysis)
        .join(MatchAnalysis, Match.id == MatchAnalysis.match_id)
    )

    if date:
        start = f"{date}T00:00:00"
        end = f"{date}T23:59:59"

        query = query.filter(
            and_(
                Match.match_date >= start,
                Match.match_date <= end
            )
        )

    rows = query.order_by(Match.match_date.asc()).all()

    results = []

    for match, analysis in rows:
        results.append({
            "match_id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "date": match.match_date[:10],
            "status": match.status,
            "markets": {
                "over_15": analysis.prob_over_15,
                "over_25": analysis.prob_over_25,
                "btts": analysis.prob_btts,
                "goal_ht": analysis.prob_goal_ht,
                "home_win": analysis.prob_home_win,
                "away_win": analysis.prob_away_win
            }
        })

    return results
