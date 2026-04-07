from sqlalchemy.orm import Session
from app.models.opportunity import Opportunity
from app.models.match import Match


class PerformanceService:

    @staticmethod
    def settle_opportunities(db: Session):

        print("📊 Liquidando oportunidades...")

        opportunities = (
            db.query(Opportunity)
            .filter(Opportunity.settled == False)
            .all()
        )

        for opp in opportunities:

            match = db.query(Match).filter(Match.id == opp.match_id).first()

            if not match or not match.is_finished:
                continue

            win = False

            if opp.market == "OVER_2_5":
                total_goals = (match.home_goals or 0) + (match.away_goals or 0)
                win = total_goals > 2.5

            elif opp.market == "BTTS":
                win = (match.home_goals or 0) > 0 and (match.away_goals or 0) > 0

            if win:
                opp.result = "WIN"
                opp.profit = opp.stake * (opp.odd - 1)
            else:
                opp.result = "LOSS"
                opp.profit = -opp.stake

            opp.settled = True

        db.commit()

        print("✅ Liquidação finalizada.")

    @staticmethod
    def calculate_roi(db: Session):

        settled = (
            db.query(Opportunity)
            .filter(Opportunity.settled == True)
            .all()
        )

        total_stake = sum(o.stake for o in settled) if settled else 0
        total_profit = sum(o.profit for o in settled) if settled else 0

        roi = (total_profit / total_stake) * 100 if total_stake > 0 else 0

        return {
            "roi_percent": round(roi, 2),
            "total_profit": round(total_profit, 2),
            "total_stake": round(total_stake, 2),
            "bets": len(settled),
        }