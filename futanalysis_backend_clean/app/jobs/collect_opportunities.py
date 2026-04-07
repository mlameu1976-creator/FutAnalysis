from datetime import date
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.opportunity import Opportunity
from app.services.thesportsdb_service import TheSportsDBService


def collect_today_opportunities():
    db: Session = SessionLocal()

    try:
        api = TheSportsDBService()

        # 🔒 Evita duplicar oportunidades do mesmo dia
        exists = (
            db.query(Opportunity)
            .filter(Opportunity.created_at == date.today())
            .first()
        )

        if exists:
            print("⚠️ Oportunidades de hoje já existem no banco.")
            return

        # ✅ USANDO O MÉTODO REAL
        events = api.get_events_by_date(date.today())

        if not events:
            print("⚠️ Nenhum jogo encontrado para hoje.")
            return

        saved = 0

        for event in events:
            normalized = api.normalize_match(event)

            home = normalized["home_team"]
            away = normalized["away_team"]

            if not home or not away:
                continue

            match_name = f"{home} x {away}"

            # 🔹 Over 1.5 (regra inicial simples)
            opp1 = Opportunity(
                match=match_name,
                market="over_1.5",
                confidence=70,
                score=70,
                source="real-engine",
            )
            db.add(opp1)
            saved += 1

            # 🔹 Over 2.5
            opp2 = Opportunity(
                match=match_name,
                market="over_2.5",
                confidence=60,
                score=60,
                source="real-engine",
            )
            db.add(opp2)
            saved += 1

            # 🔹 Casa vence
            opp3 = Opportunity(
                match=match_name,
                market="home_win",
                confidence=55,
                score=55,
                source="real-engine",
            )
            db.add(opp3)
            saved += 1

            # 🔹 Fora vence
            opp4 = Opportunity(
                match=match_name,
                market="away_win",
                confidence=55,
                score=55,
                source="real-engine",
            )
            db.add(opp4)
            saved += 1

        db.commit()
        print(f"✅ {saved} oportunidades salvas com sucesso.")

    finally:
        db.close()


if __name__ == "__main__":
    collect_today_opportunities()
