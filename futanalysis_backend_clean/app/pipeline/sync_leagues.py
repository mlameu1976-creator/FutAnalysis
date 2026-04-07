import requests
from sqlalchemy.orm import Session
from app.models.league import League

API_KEY = "844189"
API_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/all_leagues.php"


# 🔥 LIGAS TESTADAS E FUNCIONAIS
VALID_LEAGUE_IDS = {
    4328: "Premier League",
    4335: "La Liga",
    4332: "Serie A",
    4331: "Bundesliga",
    4334: "Ligue 1",
    4355: "Brasileirão",
    4346: "MLS"
}


def sync_leagues(db: Session):

    print("Sincronizando ligas (CORREÇÃO FINAL)...")

    added = 0

    for league_id, name in VALID_LEAGUE_IDS.items():

        exists = db.query(League).filter(
            League.external_id == league_id
        ).first()

        if exists:
            continue

        new_league = League(
            name=name,
            country="Unknown",
            external_id=league_id
        )

        db.add(new_league)
        added += 1

        print(f"✔ Liga adicionada: {name}")

    db.commit()

    print(f"🔥 Total ligas adicionadas: {added}")