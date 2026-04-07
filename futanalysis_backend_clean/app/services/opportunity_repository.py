from sqlalchemy.orm import Session
from app.models.opportunity import Opportunity


def save_opportunities(db: Session, opportunities_data: list):

    if not opportunities_data:
        return 0

    # 🔥 REMOVE SCORE AUTOMATICAMENTE (COMPATIBILIDADE)
    cleaned_data = []

    for item in opportunities_data:
        item = dict(item)

        # remove campos que não existem no banco
        item.pop("score", None)
        item.pop("final_score", None)
        item.pop("expected_value", None)
        item.pop("market_odds", None)
        item.pop("fair_odds", None)
        item.pop("confidence_score", None)
        item.pop("is_value_bet", None)

        cleaned_data.append(item)

    db.bulk_insert_mappings(Opportunity, cleaned_data)
    db.commit()

    return len(cleaned_data)