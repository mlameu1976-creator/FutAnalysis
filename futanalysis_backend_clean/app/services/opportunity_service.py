from sqlalchemy.orm import Session
from app.repositories.opportunity_repository import OpportunityRepository


class OpportunityService:

    def __init__(self, db: Session):
        self.repo = OpportunityRepository(db)

    def list_opportunities(self, market: str = None, day: str = None):
        return self.repo.get_opportunities(market=market, day=day)

    def get_metrics(self, day: str):
        return self.repo.get_metrics(day)

    # 🔥 NOVO
    def get_market_ranking(self, day: str, min_count: int):
        return self.repo.get_market_ranking(day, min_count)
