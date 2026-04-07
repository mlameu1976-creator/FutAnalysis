from sqlalchemy import or_
from app.models.match import Match


class TeamFormService:
    def __init__(self, db):
        self.db = db

    def get_last_matches(self, team_name: str, limit: int = 5):
        return (
            self.db.query(Match)
            .filter(
                or_(
                    Match.home_team == team_name,
                    Match.away_team == team_name
                ),
                Match.status == "Finished"
            )
            .order_by(Match.match_date.desc())
            .limit(limit)
            .all()
        )

    def calculate_form(self, team_name: str, min_games: int = 3):
        matches = self.get_last_matches(team_name)

        # 🔥 AGORA aceita times com pelo menos 3 jogos
        if len(matches) < min_games:
            return None

        stats = {
            "matches": len(matches),
            "goals_scored": 0,
            "goals_conceded": 0,
            "goals_scored_ht": 0,
            "goals_conceded_ht": 0,
        }

        for m in matches:
            is_home = m.home_team == team_name

            if is_home:
                stats["goals_scored"] += m.home_goals or 0
                stats["goals_conceded"] += m.away_goals or 0
                stats["goals_scored_ht"] += m.home_goals_ht or 0
                stats["goals_conceded_ht"] += m.away_goals_ht or 0
            else:
                stats["goals_scored"] += m.away_goals or 0
                stats["goals_conceded"] += m.home_goals or 0
                stats["goals_scored_ht"] += m.away_goals_ht or 0
                stats["goals_conceded_ht"] += m.home_goals_ht or 0

        games = stats["matches"]

        stats["avg_goals_scored"] = round(stats["goals_scored"] / games, 2)
        stats["avg_goals_conceded"] = round(stats["goals_conceded"] / games, 2)
        stats["avg_goals_scored_ht"] = round(stats["goals_scored_ht"] / games, 2)
        stats["avg_goals_conceded_ht"] = round(stats["goals_conceded_ht"] / games, 2)

        return stats