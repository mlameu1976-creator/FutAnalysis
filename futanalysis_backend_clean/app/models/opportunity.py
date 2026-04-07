from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)

    market = Column(String, nullable=False)
    probability = Column(Float, nullable=False)

    # 🔥 NOVO CAMPO (ESSENCIAL)
    score = Column(Float, nullable=True)

    # relacionamento
    match = relationship("Match", back_populates="opportunities")