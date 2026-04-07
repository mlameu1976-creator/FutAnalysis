import os
import sys
import requests
from sqlalchemy.orm import Session

# ======================================================
# AJUSTE DO PYTHONPATH
# ======================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import SessionLocal
from app.models import HistoricalMatch



# ======================================================
# CONFIGURAÇÕES
# ======================================================

API_BASE_URL = "https://api.football-data.org/v4"
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

COMPETITION_ID = 2013   # Brasileirão Série A
SEASON = 2023

HEADERS = {
    "X-Auth-Token": API_KEY
}

# ======================================================
# FUNÇÃO PRINCIPAL
# ======================================================

def load_historical_matches():
    if not API_KEY:
        raise Exception("❌ Variável de ambiente FOOTBALL_DATA_API_KEY não definida")

    print("🔄 Iniciando carga de partidas históricas...")

    url = f"{API_BASE_URL}/competitions/{COMPETITION_ID}/matches"
    params = {
        "season": SEASON,
        "status": "FINISHED"
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"❌ Erro na API: {response.status_code} - {response.text}")

    data = response.json()
    matches = data.get("matches", [])

    print(f"📥 {len(matches)} partidas encontradas na API")

    db: Session = SessionLocal()

    inserted = 0
    skipped = 0

    for match in matches:
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]

        home_goals_ft = match["score"]["fullTime"]["home"]
        away_goals_ft = match["score"]["fullTime"]["away"]

        home_goals_ht = match["score"]["halfTime"]["home"]
        away_goals_ht = match["score"]["halfTime"]["away"]

        # Proteção extra (algumas ligas retornam None)
        if home_goals_ft is None or away_goals_ft is None:
            continue

        # Evita duplicados
        exists = (
            db.query(HistoricalMatches)
            .filter(
                HistoricalMatches.competition_id == COMPETITION_ID,
                HistoricalMatches.season == SEASON,
                HistoricalMatches.home_team == home_team,
                HistoricalMatches.away_team == away_team,
                HistoricalMatches.home_goals_ft == home_goals_ft,
                HistoricalMatches.away_goals_ft == away_goals_ft,
            )
            .first()
        )

        if exists:
            skipped += 1
            continue

        historical_match = HistoricalMatches(
            competition_id=COMPETITION_ID,
            season=SEASON,
            home_team=home_team,
            away_team=away_team,
            home_goals_ft=home_goals_ft,
            away_goals_ft=away_goals_ft,
            home_goals_ht=home_goals_ht or 0,
            away_goals_ht=away_goals_ht or 0,
        )

        db.add(historical_match)
        inserted += 1

    db.commit()
    db.close()

    print("✅ Carga finalizada")
    print(f"➕ Inseridos: {inserted}")
    print(f"⏭️ Ignorados (duplicados): {skipped}")


# ======================================================
# EXECUÇÃO
# ======================================================

if __name__ == "__main__":
    load_historical_matches()
