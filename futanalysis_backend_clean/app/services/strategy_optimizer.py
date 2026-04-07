from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opportunity import Opportunity


class StrategyOptimizer:

    @staticmethod
    def optimize_filters(db: Session):

        ev_values = [0.02, 0.05, 0.08, 0.10]
        confidence_values = [0.50, 0.55, 0.60, 0.65, 0.70]
        score_values = [1, 2, 3, 4]

        best_result = None

        for ev_min in ev_values:
            for conf_min in confidence_values:
                for score_min in score_values:

                    bets = (
                        db.query(Opportunity)
                        .filter(Opportunity.settled == True)
                        .filter(Opportunity.expected_value >= ev_min)
                        .filter(Opportunity.confidence >= conf_min)
                        .filter(Opportunity.score >= score_min)
                        .all()
                    )

                    if len(bets) < 30:
                        continue

                    total_stake = sum(b.stake for b in bets)
                    total_profit = sum(b.profit for b in bets)

                    if total_stake == 0:
                        continue

                    roi = (total_profit / total_stake) * 100

                    result = {
                        "ev_min": ev_min,
                        "confidence_min": conf_min,
                        "score_min": score_min,
                        "bets": len(bets),
                        "profit": round(total_profit, 2),
                        "roi": round(roi, 2)
                    }

                    if not best_result or roi > best_result["roi"]:
                        best_result = result

        return best_result