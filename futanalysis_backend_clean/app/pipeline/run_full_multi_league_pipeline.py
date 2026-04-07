from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.pipeline.sync_historical_matches import sync_historical_matches
from app.pipeline.sync_leagues import sync_leagues
from app.pipeline.sync_matches import sync_matches
from app.pipeline.run_opportunity_pipeline import run_opportunity_pipeline
from app.services.pre_match_features_service import generate_pre_match_features


def run_pipeline():

    print("===================================")
    print("INICIANDO PIPELINE COMPLETO")
    print("===================================")

    db: Session = SessionLocal()

    try:

        print("\n1️⃣ Sincronizando ligas...")
        sync_leagues(db)

        print("\n2️⃣ Sincronizando histórico de partidas...")
        sync_historical_matches(db)

        print("\n3️⃣ Buscando jogos futuros...")
        sync_matches(db)

        print("\n4️⃣ Gerando features pré-jogo...")
        generate_pre_match_features(db)

        print("\n5️⃣ Gerando oportunidades...")
        run_opportunity_pipeline(db)

        print("\n===================================")
        print("PIPELINE FINALIZADO COM SUCESSO")
        print("===================================")

    finally:
        db.close()


if __name__ == "__main__":
    run_pipeline()
