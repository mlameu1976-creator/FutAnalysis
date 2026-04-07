from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OpportunitySchema(BaseModel):
    id: int

    # ⚠️ match_id no seu sistema atual é STRING
    match_id: Optional[str] = None

    league_id: Optional[str] = None

    home_team: Optional[str] = None
    away_team: Optional[str] = None

    market: str
    confidence: int
    score: int

    source: Optional[str] = None

    kickoff_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }