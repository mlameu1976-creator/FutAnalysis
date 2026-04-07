from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Match
from app.services.sport_api_service import SportAPIService
import time

LEAGUES = [
    {"id": 39},   # Premier League
    {"id": 140},  # La Liga
    {"id": 135},  # Serie A
    {"id": 78},   # Bundesliga
    {"id": 61},   # Ligue 1
    {"id": 88},   # Eredivisie
    {"id": 71},   # Brasileirão Série A
]


def sync_future_matches(db: Session):
    service = SportAPIService()

    db.query(Match).delete()
    db.commit()

    inserted = 0

    for league in LEAGUES:
        league_id = league["id"]

        print(f"📅 Buscando jogos futuros — liga {league_id}")

        fixtures = service.get_upcoming_matches(league_id)

        if not fixtures:
            print("⚠️ Nenhum jogo futuro encontrado")
            continue

        for f in fixtures:
            try:
                fixture = f["fixture"]
                teams = f["teams"]

                match = Match(
                    external_id=fixture["id"],
                    home_team=teams["home"]["name"],
                    away_team=teams["away"]["name"],
                    match_date=datetime.fromtimestamp(
                        fixture["timestamp"]
                    ),
                    status=fixture["status"]["short"],
                )

                db.add(match)
                inserted += 1

            except Exception as e:
                print("Erro ao inserir jogo futuro:", e)

        time.sleep(0.3)

    db.commit()
    print(f"✅ Jogos futuros inseridos: {inserted}")
    return inserted
