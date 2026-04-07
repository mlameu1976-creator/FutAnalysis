from sqlalchemy.orm import Session
from app.models.match import Match
from app.models.opportunity import Opportunity


def generate_opportunities(db: Session):

    matches = (
        db.query(Match)
        .filter(Match.is_finished == False)
        .filter(Match.home_team.isnot(None))
        .filter(Match.away_team.isnot(None))
        .filter(Match.home_team != "")
        .filter(Match.away_team != "")
        .all()
    )

    created_count = 0

    for match in matches:

        # Segurança extra
        if not match.home_team or not match.away_team:
            continue

        match_label = f"{match.home_team} vs {match.away_team}"

        base = match.id % 10

        markets = []

        if base >= 7:
            markets.append(("Over 2.5 FT", 82))

        if base >= 5:
            markets.append(("Over 1.5 FT", 75))

        if base % 2 == 0:
            markets.append(("BTTS", 70))

        if base >= 6:
            markets.append(("Casa vence", 68))

        if base <= 3:
            markets.append(("Fora vence", 66))

        if base >= 4:
            markets.append(("Goals HT", 60))

        for market_name, confidence in markets:

            existing = db.query(Opportunity).filter(
                Opportunity.match_id == match.id,
                Opportunity.market == market_name
            ).first()

            if existing:
                continue

            opportunity = Opportunity(
                match_id=match.id,
                match_label=match_label,
                market=market_name,
                confidence=confidence,
                score=round(confidence / 10),
            )

            db.add(opportunity)
            created_count += 1

    db.commit()

    return created_count