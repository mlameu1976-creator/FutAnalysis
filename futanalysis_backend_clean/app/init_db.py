from app.database import Base, engine

# IMPORTANTE:
# importe explicitamente TODOS os models que devem virar tabela
from app.models.match import Match
from app.models.team_stats import TeamStats


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Banco inicializado com sucesso (tabelas criadas)")


if __name__ == "__main__":
    init_db()