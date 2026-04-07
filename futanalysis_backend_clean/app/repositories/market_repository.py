from sqlalchemy.orm import Session
from app.models import Market


class MarketRepository:

    def __init__(self, db: Session):
        self.db = db

    def delete_by_match(self, match_id: int):
        self.db.query(Market).filter(
            Market.match_id == match_id
        ).delete()
        self.db.commit()

    def get_by_match(self, match_id: int):
        return self.db.query(Market).filter(
            Market.match_id == match_id
        ).all()

    def create(
        self,
        match_id: int,
        market: str,
        probability: float,
        expected_goals: float = None,
        home_attack: float = None,
        away_defense: float = None
    ):

        obj = Market(
            match_id=match_id,
            market=market,
            probability=probability,
            expected_goals=expected_goals,
            home_attack=home_attack,
            away_defense=away_defense
        )

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj
