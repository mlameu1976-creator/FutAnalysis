from sqlalchemy.orm import Session
from app.models.league import League


class LeagueService:

    @staticmethod
    def get_or_create(
        db: Session,
        external_id: str,
        name: str,
        country: str,
        season: str
    ) -> League:

        league = (
            db.query(League)
            .filter(
                League.external_id == external_id,
                League.season == season
            )
            .first()
        )

        if league:
            return league

        league = League(
            external_id=external_id,
            name=name,
            country=country,
            season=season
        )

        db.add(league)
        db.commit()
        db.refresh(league)

        return league