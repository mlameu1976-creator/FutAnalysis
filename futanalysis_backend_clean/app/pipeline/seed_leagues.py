from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.league import League


LEAGUES = [
    {"external_id": 4351, "name": "Brazil Serie B", "country": "Brazil"},
    {"external_id": 4332, "name": "Bundesliga 2", "country": "Germany"},
    {"external_id": 4333, "name": "Bundesliga 3", "country": "Germany"},
    {"external_id": 4335, "name": "La Liga 2", "country": "Spain"},
    {"external_id": 4337, "name": "Eerste Divisie", "country": "Netherlands"},
    {"external_id": 4356, "name": "A-League", "country": "Australia"},
    {"external_id": 4338, "name": "Austrian Bundesliga", "country": "Austria"},
    {"external_id": 4339, "name": "TFF First League", "country": "Turkey"},
    {"external_id": 4334, "name": "Ligue 2", "country": "France"},
    {"external_id": 4344, "name": "Liga Portugal 2", "country": "Portugal"},
    {"external_id": 4358, "name": "OBOS-ligaen", "country": "Norway"},
    {"external_id": 4400, "name": "Argentina Primera Division", "country": "Argentina"},
    {"external_id": 4951, "name": "Colombia Primera A", "country": "Colombia"},
    {"external_id": 4350, "name": "Liga MX", "country": "Mexico"},
    {"external_id": 4401, "name": "Uruguay Primera Division", "country": "Uruguay"},
]


def seed_leagues():

    db: Session = SessionLocal()

    created = 0

    for league_data in LEAGUES:

        exists = db.query(League).filter(
            League.external_id == int(league_data["external_id"])
        ).first()

        if exists:
            continue

        league = League(
            external_id=int(league_data["external_id"]),  # 🔥 FORÇA INT
            name=str(league_data["name"]),
            country=str(league_data["country"]),
        )

        db.add(league)
        created += 1

    db.commit()
    db.close()

    print(f"✅ Ligas criadas: {created}")


if __name__ == "__main__":
    seed_leagues()