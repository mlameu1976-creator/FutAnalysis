from datetime import datetime
from app.database import SessionLocal
from app.services.thesportsdb_client import TheSportsDBClient
from app.services.match_service import MatchService
from app.config.leagues import LEAGUES


def parse_date(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def run():
    db = SessionLocal()
    service = MatchService(db)
    client = TheSportsDBClient()

    total_saved = 0

    for league_name, league_id in LEAGUES.items():
        events = client.get_last_events_by_league(league_id)

        for e in events:
            if not e.get("idEvent") or not e.get("dateEvent"):
                continue

            saved = service.create_or_ignore({
                "external_id": e["idEvent"],
                "league_id": league_id,
                "league_name": league_name,
                "season": e.get("strSeason"),
                "match_date": parse_date(e["dateEvent"]),
                "home_team": e.get("strHomeTeam"),
                "away_team": e.get("strAwayTeam"),
                "home_goals": int(e["intHomeScore"]) if e.get("intHomeScore") else None,
                "away_goals": int(e["intAwayScore"]) if e.get("intAwayScore") else None,
                "home_goals_ht": int(e["intHomeScoreHT"]) if e.get("intHomeScoreHT") else None,
                "away_goals_ht": int(e["intAwayScoreHT"]) if e.get("intAwayScoreHT") else None,
                "status": e.get("strStatus", "Unknown"),
            })

            if saved:
                total_saved += 1

        print(f"[OK] {league_name}: {len(events)} eventos processados")

    db.close()
    print(f"✅ Total de jogos novos salvos: {total_saved}")


if __name__ == "__main__":
    run()