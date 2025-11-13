from sqlmodel import SQLModel, Field
from typing import Optional
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: Optional[str]
    title: str
    competition: Optional[str]
    date: Optional[str]
    home: Optional[str]
    away: Optional[str]
    score: Optional[str]
    thumbnail: Optional[str]
    embed: Optional[str]
    raw_json: Optional[str]
