import os
import requests
from sqlalchemy.orm import Session

from app.models import Team


class FootballDataTeamService:
    def __init__(self, db: Session):
        self.db = db
        self.base_url = "https://api.football-data.org/v4"

        api_key = os.getenv("FOOTBALL_DATA_API_KEY")
        if not api_key:
            raise RuntimeError("FOOTBALL_DATA_API_KEY não configurada")

        self.headers = {
            "X-Auth-Token": api_key
        }

    def sync_teams_from_competition(self, competition_code: str):
        """
        Ex: PL, SA, PD, BL1, FL1
        """
        url = f"{self.base_url}/competitions/{competition_code}/teams"
        r = requests.get(url, headers=self.headers, timeout=20)
        r.raise_for_status()

        teams = r.json().get("teams", [])

        for t in teams:
            name = t["name"]
            fd_id = t["id"]

            exists = self.db.query(Team).filter(Team.name == name).first()
            if exists:
                exists.football_data_id = fd_id
            else:
                self.db.add(
                    Team(
                        name=name,
                        football_data_id=fd_id
                    )
                )

        self.db.commit()
