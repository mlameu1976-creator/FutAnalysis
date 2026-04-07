import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(BASE_DIR)

# IMPORT DO MÓDULO REAL
from app.services import thesportsdb_season_ingest_service as ingest_module


HISTORICAL_CONFIGS = [
    {
        "LEAGUE_ID": "4328",
        "SEASON": "2024-2025",
        "LEAGUE_NAME": "Premier League",
    },
    {
        "LEAGUE_ID": "4335",
        "SEASON": "2025",
        "LEAGUE_NAME": "Brazilian Serie A",
    },
    {
        "LEAGUE_ID": "4346",
        "SEASON": "2025",
        "LEAGUE_NAME": "Major League Soccer",
    },
    {
        "LEAGUE_ID": "4396",
        "SEASON": "2025",
        "LEAGUE_NAME": "Norwegian Eliteserien",
    },
    {
        "LEAGUE_ID": "4687",
        "SEASON": "2024-2025",
        "LEAGUE_NAME": "Saudi Pro League",
    },
]


def run():
    for cfg in HISTORICAL_CONFIGS:
        print(
            f"\nIngesting historical matches | "
            f"{cfg['LEAGUE_NAME']} ({cfg['SEASON']})"
        )

        # 🔴 SETA VARIÁVEIS GLOBAIS QUE O SCRIPT USA
        ingest_module.LEAGUE_ID = cfg["LEAGUE_ID"]
        ingest_module.SEASON = cfg["SEASON"]

        # EXECUTA A FUNÇÃO REAL
        ingest_module.ingest_season_matches()

    print("\nHistorical ingest finished successfully.")


if __name__ == "__main__":
    run()