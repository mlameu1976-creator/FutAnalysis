from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import SessionLocal
from app.models.match import Match
from app.models.opportunity import Opportunity
from app.services.recent_form_analyzer import calculate_team_form


# Status aceitos como jogos futuros
VALID_FUTURE_STATUS = [
    "Scheduled",
    "Not Started",
    "NS",
    "TIMED",
]


def calculate_score(confidence: int) -> int:
    return int(confidence * 1.15)


def run():
    print(">>> FUTANALYSIS – GENERATE OPPORTUNITIES (RECENT FORM ENGINE – BALANCED) <<<")

    db: Session = SessionLocal()

    try:
        matches = (
            db.query(Match)
            .filter(Match.status.in_(VALID_FUTURE_STATUS))
            .all()
        )

        print(f"[DEBUG] Jogos futuros considerados: {len(matches)}")

        created = 0

        for match in matches:
            home_form = calculate_team_form(db, match.home_team)
            away_form = calculate_team_form(db, match.away_team)

            # Agora aceita times com pelo menos 3 jogos
            if not home_form or not away_form:
                continue

            market_confidence = {}

            # Over 1.5 FT
            avg_goals = home_form["avg_goals_for"] + away_form["avg_goals_for"]
            over15_rate = (home_form["over_15_rate"] + away_form["over_15_rate"]) / 2
            conf = 50
            if avg_goals >= 2.2:
                conf += 10
            if over15_rate >= 0.6:
                conf += 8
            market_confidence["Over 1.5 FT"] = conf

            # Over 2.5 FT
            conf = 45
            if avg_goals >= 2.7:
                conf += 12
            if (home_form["over_25_rate"] + away_form["over_25_rate"]) / 2 >= 0.55:
                conf += 8
            market_confidence["Over 2.5 FT"] = conf

            # Goals HT
            conf = 45
            if home_form["avg_goals_for"] >= 1.1 or away_form["avg_goals_for"] >= 1.1:
                conf += 8
            market_confidence["Goals HT"] = conf

            # BTTS
            conf = 45
            if (home_form["btts_rate"] + away_form["btts_rate"]) / 2 >= 0.55:
                conf += 12
            if home_form["avg_goals_against"] >= 1 and away_form["avg_goals_against"] >= 1:
                conf += 8
            market_confidence["BTTS"] = conf

            # Casa vence
            diff = home_form["avg_goals_for"] - away_form["avg_goals_against"]
            market_confidence["Casa vence"] = 45 + int(diff * 8)

            # Fora vence
            diff = away_form["avg_goals_for"] - home_form["avg_goals_against"]
            market_confidence["Fora vence"] = 45 + int(diff * 8)

            for market, confidence in market_confidence.items():
                if confidence < 50:
                    continue  # filtro equilibrado

                opportunity = Opportunity(
                    match=f"{match.home_team} vs {match.away_team}",
                    market=market,
                    confidence=int(min(confidence, 90)),
                    score=calculate_score(confidence),
                    source="recent_form_engine_balanced",
                    kickoff=match.match_date,
                    created_at=datetime.utcnow(),
                )

                db.add(opportunity)
                created += 1

        db.commit()
        print(f"[DEBUG] Oportunidades criadas: {created}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run()