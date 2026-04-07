import os
import sys

from dotenv import load_dotenv

# carrega SEMPRE o .env
load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.league import League
from app.services.team_stats_service import TeamStatsService
from app.services.pre_match_features_service import PreMatchFeaturesService
from app.services.opportunity_engine import OpportunityEngine


def run():
    print("DATABASE:", engine.url)

    db: Session = SessionLocal()

    try:
        leagues = db.query(League).all()

        if not leagues:
            print("No leagues found.")
            return

        for league in leagues:
            print(f"Processing league: {league.name} ({league.season})")

            TeamStatsService.rebuild_for_league(
                db=db,
                league_id=league.id,
                season=league.season
            )

            PreMatchFeaturesService.build_for_league(
                db=db,
                league_id=league.id,
                season=league.season
            )

            OpportunityEngine.run_for_league(
                db=db,
                league_id=league.id,
                season=league.season
            )

        print("Pipeline finished successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    run()