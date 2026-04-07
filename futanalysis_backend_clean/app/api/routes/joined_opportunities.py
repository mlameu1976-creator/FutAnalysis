from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.match import Match
from app.models.league import League
from app.models.pre_match_features import PreMatchFeatures
from app.models.opportunity import Opportunity

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard/opportunities/joined")
def get_joined_opportunities(db: Session = Depends(get_db)):
    results = (
        db.query(
            Match.id.label("match_id"),
            Match.match_date,
            Match.home_team,
            Match.away_team,

            League.name.label("league"),
            League.country,
            League.season,

            PreMatchFeatures.exp_home_goals,
            PreMatchFeatures.exp_away_goals,
            PreMatchFeatures.exp_total_goals,
            PreMatchFeatures.prob_btts,
            PreMatchFeatures.prob_over_15,
            PreMatchFeatures.prob_over_25,
            PreMatchFeatures.prob_goal_ht,

            Opportunity.market,
            Opportunity.score,
            Opportunity.confidence,
        )
        # League é obrigatória
        .join(League, League.id == Match.league_id)

        # Features e oportunidades podem não existir
        .outerjoin(
            PreMatchFeatures,
            PreMatchFeatures.match_id == Match.id
        )
        .outerjoin(
            Opportunity,
            Opportunity.match_id == Match.id
        )

        .filter(Match.is_finished.is_(False))
        .order_by(Opportunity.score.desc().nullslast())
        .limit(100)
        .all()
    )

    return [
        {
            "match_id": r.match_id,
            "date": r.match_date,
            "league": f"{r.league} ({r.season})",
            "home_team": r.home_team,
            "away_team": r.away_team,

            "expected_goals": {
                "home": r.exp_home_goals,
                "away": r.exp_away_goals,
                "total": r.exp_total_goals,
                "ht_goal_prob": r.prob_ht_goal,
            },

            "probabilities": {
                "btts": r.prob_btts,
                "over_15": r.prob_over_15,
                "over_25": r.prob_over_25,
            },

            "opportunity": None
            if r.market is None
            else {
                "market": r.market,
                "score": r.score,
                "confidence": r.confidence,
            },
        }
        for r in results
    ]