from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.match import Match
from app.services.pre_match_features_service import PreMatchFeaturesService


def generate_pre_match_features():

    print("GERANDO FEATURES FUTANALYSIS...")

    db: Session = SessionLocal()

    service = PreMatchFeaturesService(db)

    matches = db.query(Match).all()

    total = len(matches)

    print(f"TOTAL MATCHES ENCONTRADOS: {total}")

    processed = 0

    for match in matches:

        service.generate_features_for_match(match)

        processed += 1

        if processed % 1000 == 0:
            print(f"{processed} matches processados")

    db.commit()

    print(f"PROCESSAMENTO FINALIZADO: {processed}")


def run():
    generate_pre_match_features()


if __name__ == "__main__":
    run()