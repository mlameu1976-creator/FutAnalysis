from sqlalchemy.orm import Session
from datetime import datetime

from app.models import HistoricalMatch
from app.models import Team
from app.services.sportapi_history_service import SportAPIHistoryService


def sync_historical_matches(db: Session):
    # 🔥 INSTANCIA AQUI (NÃO NO TOPO)
    service = SportAPIHistoryService()

    print("🔄 Limpando histórico antigo...")
    db.query(HistoricalMatch).delete()
    db.commit()

    teams = db.query(Team).all()
    inserted = 0

    print(f"⚽ Buscando histórico de {len(teams)} times (10 jogos cada)")

    for team in teams:
        try:
            matches = service.get_last_matches(team.external_id, limit=10)
        except Exception as e:
            print(f"❌ Erro no time {team.name}: {e}")
            continue

        for m in matches:
            fixture = m.get("fixture")
            goals = m.get("goals")
            teams_data = m.get("teams")

            if not fixture or not goals or goals.get("home") is None:
                continue

            is_home = teams_data["home"]["id"] == team.external_id

            record = HistoricalMatch(
                team=team.name,
                opponent=teams_data["away" if is_home else "home"]["name"],
                is_home=is_home,
                goals_for=goals["home"] if is_home else goals["away"],
                goals_against=goals["away"] if is_home else goals["home"],
                goals_for_ht=m["score"]["halftime"]["home"]
                    if is_home else m["score"]["halftime"]["away"],
                goals_against_ht=m["score"]["halftime"]["away"]
                    if is_home else m["score"]["halftime"]["home"],
                match_date=datetime.fromisoformat(fixture["date"]).date(),
                status=fixture["status"]["short"]
            )

            db.add(record)
            inserted += 1

    db.commit()
    print(f"✅ Histórico inserido: {inserted}")

    return inserted
