from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.league import League
from app.services.thesportsdb_season_ingest_service import ingest_league_season


def run_historical_ingest_targeted():

    db: Session = SessionLocal()

    print("Baixando histórico das ligas...")

    leagues = db.query(League).all()

    print(f"Ligas encontradas: {len(leagues)}")

    for league in leagues:

        print(f"Baixando histórico da liga {league.name} - 2024-2025")
        ingest_league_season(db, league.external_id, "2024-2025")

        print(f"Baixando histórico da liga {league.name} - 2023-2024")
        ingest_league_season(db, league.external_id, "2023-2024")

    db.close()