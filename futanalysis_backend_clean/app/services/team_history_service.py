from sqlalchemy.orm import Session
from app.database import get_db
from app.models import HistoricalMatch


class TeamHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_last_matches(self, team_name: str, limit: int = 5):
        return (
            self.db.query(HistoricalMatch)
            .filter(
                (HistoricalMatch.home_team == team_name)
                | (HistoricalMatch.away_team == team_name)
            )
            .order_by(HistoricalMatch.id.desc())  # ✅ USANDO ID
            .limit(limit)
            .all()
        )
