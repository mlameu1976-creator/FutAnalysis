from datetime import date
from sqlalchemy.orm import Session
from app.models.match import Match


class MatchService:
    def __init__(self, db: Session):
        self.db = db

    # 🔥 NOVO MÉTODO – ESSENCIAL
    def get_future_matches(self):
        today = date.today()

        return (
            self.db.query(Match)
            .filter(Match.match_date >= today)
            .filter(Match.status.in_(["Scheduled", "Not Started", None]))
            .all()
        )

    # Mantém compatibilidade com o resto do sistema
    def create_or_ignore(self, data: dict) -> bool:
        exists = (
            self.db.query(Match)
            .filter(Match.external_id == data["external_id"])
            .first()
        )

        if exists:
            return False

        match = Match(**data)
        self.db.add(match)
        self.db.commit()
        return True