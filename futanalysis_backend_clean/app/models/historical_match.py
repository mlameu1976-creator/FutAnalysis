from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class HistoricalMatch(Base):
    __tablename__ = "historical_matches"

    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(Integer, index=True)
    season = Column(Integer)

    date = Column(Date, index=True)

    home_team = Column(String, index=True)
    away_team = Column(String, index=True)

    home_goals = Column(Integer)
    away_goals = Column(Integer)
