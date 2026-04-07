from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    UniqueConstraint
)
from app.database import Base


class TeamStats(Base):
    __tablename__ = "team_stats"

    id = Column(Integer, primary_key=True, index=True)

    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    season = Column(String, nullable=False)

    team_name = Column(String, nullable=False)

    matches_played = Column(Integer, default=0)

    # GOLS
    goals_scored_avg = Column(Float, default=0.0)
    goals_conceded_avg = Column(Float, default=0.0)

    goals_scored_home_avg = Column(Float, default=0.0)
    goals_conceded_home_avg = Column(Float, default=0.0)

    goals_scored_away_avg = Column(Float, default=0.0)
    goals_conceded_away_avg = Column(Float, default=0.0)

    # MERCADOS
    btts_rate = Column(Float, default=0.0)
    over_15_rate = Column(Float, default=0.0)
    over_25_rate = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint(
            "league_id",
            "season",
            "team_name",
            name="uq_team_league_season"
        ),
    )

    def __repr__(self):
        return f"<TeamStats {self.team_name} ({self.season})>"