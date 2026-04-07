from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class PreMatchFeatures(Base):

    __tablename__ = "pre_match_features"

    id = Column(Integer, primary_key=True)

    match_id = Column(Integer, ForeignKey("matches.id"))

    # gols esperados
    exp_home_goals = Column(Float)
    exp_away_goals = Column(Float)
    exp_total_goals = Column(Float)

    # probabilidades
    prob_btts = Column(Float)
    prob_over_15 = Column(Float)
    prob_over_25 = Column(Float)

    prob_goal_ht = Column(Float)

    prob_home_win = Column(Float)
    prob_away_win = Column(Float)
    prob_under_25 = Column(Float)

    match = relationship("Match")