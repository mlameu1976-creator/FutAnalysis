from sqlalchemy.orm import Session
from app.models import Team
from app.services.sportapi_team_service import SportAPITeamService
from app.config.leagues import LEAGUE_SEASONS


def sync_teams(db: Session):
    db.query(Team).delete()
    db.commit()

    service = SportAPITeamService()
    inserted = 0

    for league_name, season_id in LEAGUE_SEASONS.items():
        print(f"⚽ Buscando times - {league_name} (season {season_id})")

        teams = service.get_teams_by_season(season_id)

        for t in teams:
            team = Team(
                name=t["name"],
                external_id=t["id"],
                league=league_name
            )
            db.add(team)
            inserted += 1

    db.commit()
    print(f"✅ Total de times inseridos: {inserted}")
    return inserted
