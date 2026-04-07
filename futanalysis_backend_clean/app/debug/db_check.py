from app.database import SessionLocal
from app.models import HistoricalMatch
from sqlalchemy import func

db = SessionLocal()

print("TOTAL DE REGISTROS:", db.query(HistoricalMatch).count())

print("\nTOP 10 TIMES POR QTDE DE JOGOS:")
res = (
    db.query(
        HistoricalMatch.team,
        func.count(HistoricalMatch.id)
    )
    .group_by(HistoricalMatch.team)
    .order_by(func.count(HistoricalMatch.id).desc())
    .limit(10)
    .all()
)

for r in res:
    print(r)

print("\nEXEMPLO DE REGISTROS:")
sample = db.query(HistoricalMatch).limit(5).all()
for m in sample:
    print(
        m.team,
        m.goals_for,
        m.goals_against,
        m.match_date
    )
