from sqlalchemy.orm import Session

from app.models.match import Match


class TeamStatsService:

    def __init__(self, db: Session):

        self.db = db

        self.strengths = self.get_team_attack_defense_strength()

    def get_team_attack_defense_strength(self):

        matches = self.db.query(Match).filter(
            Match.is_finished == True
        ).all()

        stats = {}

        for match in matches:

            home = match.home_team
            away = match.away_team

            home_goals = match.home_goals or 0
            away_goals = match.away_goals or 0

            if home not in stats:
                stats[home] = {
                    "scored": 0,
                    "conceded": 0,
                    "games": 0
                }

            if away not in stats:
                stats[away] = {
                    "scored": 0,
                    "conceded": 0,
                    "games": 0
                }

            stats[home]["scored"] += home_goals
            stats[home]["conceded"] += away_goals
            stats[home]["games"] += 1

            stats[away]["scored"] += away_goals
            stats[away]["conceded"] += home_goals
            stats[away]["games"] += 1

        strengths = {}

        for team, data in stats.items():

            games = data["games"] or 1

            strengths[team] = {
                "attack": data["scored"] / games,
                "defense": data["conceded"] / games
            }

        return strengths
