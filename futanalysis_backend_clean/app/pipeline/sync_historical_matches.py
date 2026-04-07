from sqlalchemy.orm import Session
from app.models.league import League
from app.services.historical_ingest_service import ingest_historical_matches


# 🔥 FUNÇÃO INTELIGENTE DE TEMPORADAS
def get_seasons_for_league(league_name: str):

    if not league_name:
        return []

    name = league_name.lower()

    # 🔥 ligas com calendário anual
    yearly_keywords = [
        "brazil",
        "brasileiro",
        "mls",
        "japan",
        "china",
        "sweden",
        "norway",
        "argentina",
        "usa",
    ]

    # 🔥 temporadas padrão (europa)
    seasons = [
        "2020-2021",
        "2021-2022",
        "2022-2023",
        "2023-2024",
        "2024-2025",
        "2025-2026"
    ]

    # 🔥 adiciona formato anual se necessário
    if any(k in name for k in yearly_keywords):
        seasons.extend([
            "2021",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026"
        ])

    return seasons


def sync_historical_matches(db: Session):

    print("Sincronizando histórico de partidas...")

    leagues = db.query(League).all()

    total_inserted = 0

    for league in leagues:

        if not league.external_id:
            continue

        seasons = get_seasons_for_league(league.name)

        print(f"\n🏆 Liga: {league.name}")

        for season in seasons:

            try:
                print(f"📅 Temporada: {season}")

                inserted = ingest_historical_matches(
                    db,
                    league.external_id,
                    season
                )

                total_inserted += inserted

            except Exception as e:
                print(f"Erro na liga {league.name} temporada {season}: {e}")
                continue

    print(f"\n🔥 Total jogos históricos inseridos: {total_inserted}")

    return total_inserted