from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opportunity import Opportunity
from app.models.match import Match


class PerformanceAnalyzer:

    # ==========================================
    # ROI POR MERCADO
    # ==========================================

    @staticmethod
    def roi_by_market(db: Session):

        results = (
            db.query(
                Opportunity.market,
                func.count(Opportunity.id),
                func.sum(Opportunity.profit),
                func.sum(Opportunity.stake),
            )
            .filter(Opportunity.settled == True)
            .group_by(Opportunity.market)
            .all()
        )

        data = []

        for market, bets, profit, stake in results:

            roi = (profit / stake) * 100 if stake else 0

            data.append({
                "market": market,
                "bets": bets,
                "profit": round(profit or 0, 2),
                "roi": round(roi, 2)
            })

        return data

    # ==========================================
    # ROI POR LIGA
    # ==========================================

    @staticmethod
    def roi_by_league(db: Session):

        results = (
            db.query(
                Match.league_id,
                func.count(Opportunity.id),
                func.sum(Opportunity.profit),
                func.sum(Opportunity.stake),
            )
            .join(Match, Match.id == Opportunity.match_id)
            .filter(Opportunity.settled == True)
            .group_by(Match.league_id)
            .all()
        )

        data = []

        for league, bets, profit, stake in results:

            roi = (profit / stake) * 100 if stake else 0

            data.append({
                "league_id": league,
                "bets": bets,
                "profit": round(profit or 0, 2),
                "roi": round(roi, 2)
            })

        return data

    # ==========================================
    # ROI POR SCORE
    # ==========================================

    @staticmethod
    def roi_by_score(db: Session):

        results = (
            db.query(
                Opportunity.score,
                func.count(Opportunity.id),
                func.sum(Opportunity.profit),
                func.sum(Opportunity.stake),
            )
            .filter(Opportunity.settled == True)
            .group_by(Opportunity.score)
            .all()
        )

        data = []

        for score, bets, profit, stake in results:

            roi = (profit / stake) * 100 if stake else 0

            data.append({
                "score": score,
                "bets": bets,
                "profit": round(profit or 0, 2),
                "roi": round(roi, 2)
            })

        return data

    # ==========================================
    # CURVA DE BANCA (LIMITADA)
    # ==========================================

    @staticmethod
    def bankroll_curve(db: Session):

        results = (
            db.query(Opportunity)
            .filter(Opportunity.settled == True)
            .order_by(Opportunity.id)
            .limit(500)   # 🔥 LIMITA PARA NÃO QUEBRAR O SWAGGER
            .all()
        )

        bankroll = 0
        curve = []

        for i, bet in enumerate(results):

            profit = bet.profit or 0

            bankroll += profit

            curve.append({
                "bet_number": i + 1,
                "profit": round(profit, 2),
                "bankroll": round(bankroll, 2)
            })

        return curve