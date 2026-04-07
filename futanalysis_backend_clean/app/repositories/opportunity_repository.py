from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opportunity import Opportunity
from app.models.match import Match


class OpportunityRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_opportunities(self, market: str | None = None, day: str | None = None):

        query = (
            self.db.query(Opportunity)
            .join(Match, Match.id == Opportunity.match_id)
        )

        # filtro de mercado
        if market and market != "all":
            query = query.filter(Opportunity.market == market)

        # filtro por dia
        query = self._apply_day_filter(query, day)

        return query.order_by(Match.match_date.asc()).all()

    def _apply_day_filter(self, query, day: str | None):

        today = date.today()

        if day == "today":

            query = query.filter(
                func.date(Match.match_date) == today
            )

        elif day == "tomorrow":

            tomorrow = today + timedelta(days=1)

            query = query.filter(
                func.date(Match.match_date) == tomorrow
            )

        return query