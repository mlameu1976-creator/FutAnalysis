from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class OpportunityResult(Base):
    __tablename__ = "opportunity_results"

    id = Column(Integer, primary_key=True, index=True)

    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    result = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    opportunity = relationship("Opportunity")

    def __repr__(self):
        return f"<OpportunityResult {self.id} - {self.result}>"