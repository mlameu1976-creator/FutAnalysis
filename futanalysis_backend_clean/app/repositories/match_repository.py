from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import date

from app.models.match import Match


class MatchRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_external_id(self, external_id: str) -> Match | None:
        return (
            self.db.query(Match)
            .filter(Match.external_id == external_id)
            .first()
        )

    def save(self, match: Match) -> Match:
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match

    def get_matches(
        self,
        team: Optional[str] = None,
        league: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        limit: int = 50,
    ) -> List[Match]:
        q = self.db.query(Match)

        if team:
            q = q.filter(
                or_(
                    Match.home_team == team,
                    Match.away_team == team
                )
            )

        if league:
            q = q.filter(Match.league_name == league)

        if from_date:
            q = q.filter(Match.match_date >= from_date)

        if to_date:
            q = q.filter(Match.match_date <= to_date)

        return (
            q.order_by(Match.match_date.desc())
            .limit(limit)
            .all()
        )

    def get_last_matches_by_team(self, team: str, limit: int = 5) -> List[Match]:
        return (
            self.db.query(Match)
            .filter(
                and_(
                    or_(
                        Match.home_team == team,
                        Match.away_team == team
                    ),
                    Match.is_finished.is_(True)
                )
            )
            .order_by(Match.match_date.desc())
            .limit(limit)
            .all()
        )