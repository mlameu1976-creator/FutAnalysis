from sqlalchemy.orm import Session
from app.models import TeamStats


class TeamStatsRepository:

    def get_by_team(self, db: Session, team_name: str):
        return db.query(TeamStats).filter(
            TeamStats.team_name == team_name
        ).first()

    # ✅ NOVO MÉTODO
    def get_all(self, db: Session):
        return db.query(TeamStats).all()

    def create_or_update(
        self,
        db: Session,
        team_name: str,
        home_matches: int,
        home_goals_for: int,
        home_goals_against: int,
        away_matches: int,
        away_goals_for: int,
        away_goals_against: int
    ):

        home_avg_for = home_goals_for / home_matches if home_matches else 0
        home_avg_against = home_goals_against / home_matches if home_matches else 0

        away_avg_for = away_goals_for / away_matches if away_matches else 0
        away_avg_against = away_goals_against / away_matches if away_matches else 0

        team = self.get_by_team(db, team_name)

        if team:
            team.home_matches = home_matches
            team.home_goals_for = home_goals_for
            team.home_goals_against = home_goals_against
            team.home_avg_for = home_avg_for
            team.home_avg_against = home_avg_against

            team.away_matches = away_matches
            team.away_goals_for = away_goals_for
            team.away_goals_against = away_goals_against
            team.away_avg_for = away_avg_for
            team.away_avg_against = away_avg_against
        else:
            team = TeamStats(
                team_name=team_name,

                home_matches=home_matches,
                home_goals_for=home_goals_for,
                home_goals_against=home_goals_against,
                home_avg_for=home_avg_for,
                home_avg_against=home_avg_against,

                away_matches=away_matches,
                away_goals_for=away_goals_for,
                away_goals_against=away_goals_against,
                away_avg_for=away_avg_for,
                away_avg_against=away_avg_against
            )
            db.add(team)

        db.commit()
        return team
