from app.services.thesportsdb_future_ingest_service import ingest_future_matches


def sync_matches(db):

    print("Buscando jogos futuros...")

    # 🔥 CORREÇÃO AQUI → PASSANDO O DB
    created = ingest_future_matches(db)

    print(f"Jogos futuros inseridos/atualizados: {created}")

    return created