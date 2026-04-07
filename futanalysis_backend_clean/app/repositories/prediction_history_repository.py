from sqlalchemy.orm import Session
from typing import List

from app.models import PredictionHistory


class PredictionHistoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        match_id: int,
        market: str,
        probability: float,
        result: str = "PENDING"
    ) -> PredictionHistory:

        record = PredictionHistory(
            match_id=match_id,
            market=market,
            probability=probability,
            result=result
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record

    def get_all(self) -> List[PredictionHistory]:
        return self.db.query(PredictionHistory).all()
