from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.database import SessionLocal
from app.services.evaluation_service import evaluate_pending_opportunities
from app.services.thesportsdb_service import sync_matches

scheduler = BackgroundScheduler()

def daily_job():
    db = SessionLocal()
    try:
        print("🔄 Running daily evaluation job...")
        sync_matches(db)
        evaluate_pending_opportunities(db)
        print("✅ Daily job completed:", datetime.now())
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(daily_job, 'cron', hour=3, minute=0)
    scheduler.start()