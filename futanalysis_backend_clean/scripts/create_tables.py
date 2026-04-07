import sys
import os

# 🔥 força o Python a enxergar a raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# 🔥 IMPORTAR TODOS OS MODELS
from app.models.match import Match
from app.models.league import League
from app.models.pre_match_features import PreMatchFeatures
from app.models.team_stats import TeamStats
from app.models.opportunity import Opportunity

# 🔥 URL DIRETA (GARANTIDA)
DATABASE_URL = "postgresql://postgres:452576@localhost:5432/futanalysis"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# 🔥 VINCULAR METADATA DOS MODELS
Base.metadata = Match.metadata


def create_tables():
    print("🚀 Criando tabelas...")

    Base.metadata.create_all(bind=engine)

    print("✅ Tabelas criadas com sucesso")


if __name__ == "__main__":
    create_tables()