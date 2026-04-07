from app.database import SessionLocal
from app.models.opportunity import Opportunity


def cleanup_opportunities():
    db = SessionLocal()

    try:
        deleted = (
            db.query(Opportunity)
            .filter(Opportunity.kickoff.is_(None))
            .delete(synchronize_session=False)
        )

        db.commit()
        print(f"🧹 {deleted} oportunidades com kickoff NULL removidas.")

    finally:
        db.close()


if __name__ == "__main__":
    cleanup_opportunities()