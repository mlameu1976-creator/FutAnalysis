from datetime import datetime, timedelta
from app.database import SessionLocal
from app.services.thesportsdb_client import TheSportsDBClient
from app.services.match_service import MatchService


def run():
    db = SessionLocal()
    service = MatchService(db)
    client = TheSportsDBClient()

    total_saved = 0
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    days_to_collect = [
        ("HOJE", today),
        ("AMANHÃ", tomorrow),
    ]

    for label, day in days_to_collect:
        date_str = day.strftime("%Y-%m-%d")
        print(f"\n📅 Coletando jogos de {label} ({date_str})")

        events = client.get_events_by_day(date_str)
        print(f"[DAY {date_str}] eventos recebidos: {len(events)}")

        for e in events:
            # Ignorar eventos inválidos
            if not e.get("idEvent") or not e.get("dateEvent"):
                continue

            # Ignorar jogos já finalizados
            status = e.get("strStatus")
            if status and status.lower() in ["finished", "ft"]:
                continue

            saved = service.create_or_ignore({
                "external_id": e["idEvent"],
                "league_id": e.get("idLeague"),
                "league_name": e.get("strLeague"),
                "season": e.get("strSeason"),
                "match_date": day,
                "home_team": e.get("strHomeTeam"),
                "away_team": e.get("strAwayTeam"),

                # Placar FULL TIME (normalmente vazio para jogos futuros)
                "home_goals": int(e["intHomeScore"]) if e.get("intHomeScore") else None,
                "away_goals": int(e["intAwayScore"]) if e.get("intAwayScore") else None,

                # 🔥 GOLS HT (incluído conforme solicitado)
                "home_goals_ht": int(e["intHomeScoreHT"]) if e.get("intHomeScoreHT") else None,
                "away_goals_ht": int(e["intAwayScoreHT"]) if e.get("intAwayScoreHT") else None,

                "status": status or "Scheduled",
            })

            if saved:
                total_saved += 1

    db.close()
    print(f"\n✅ Total de jogos FUTUROS salvos: {total_saved}")


if __name__ == "__main__":
    run()