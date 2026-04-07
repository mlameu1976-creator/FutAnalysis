from datetime import date
from typing import Optional
from pydantic import BaseModel


class MatchOut(BaseModel):
    id: int
    external_id: str

    league_id: str
    league_name: str
    season: Optional[str]

    match_date: date

    home_team: str
    away_team: str

    home_goals: Optional[int]
    away_goals: Optional[int]
    home_goals_ht: Optional[int]
    away_goals_ht: Optional[int]

    status: str

    is_finished: bool
    is_draw: Optional[bool]
    home_win: Optional[bool]
    away_win: Optional[bool]
    btts: Optional[bool]
    over_15: Optional[bool]
    over_25: Optional[bool]

    class Config:
        orm_mode = True