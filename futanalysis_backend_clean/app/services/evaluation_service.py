from datetime import datetime
from app.models.opportunity import Opportunity
from app.models.match import Match
from app.models.opportunity_result import OpportunityResult

def evaluate_pending_opportunities(db):

    pending = db.query(Opportunity).join(Match).filter(
        Match.is_finished == True
    ).all()

    for opp in pending:

        match = opp.match

        total_goals = match.home_goals + match.away_goals

        result = "loss"

        if opp.market == "Over 2.5 FT" and total_goals > 2:
            result = "win"

        if opp.market == "Over 1.5 FT" and total_goals > 1:
            result = "win"

        if opp.market == "BTTS" and match.home_goals > 0 and match.away_goals > 0:
            result = "win"

        if opp.market == "Casa vence" and match.home_goals > match.away_goals:
            result = "win"

        profit = 0
        if result == "win":
            profit = 0.8  # odd 1.80 - stake 1
        else:
            profit = -1

        result_record = OpportunityResult(
            opportunity_id=opp.id,
            result=result,
            profit=profit,
            evaluated_at=datetime.now()
        )

        db.add(result_record)

    db.commit()