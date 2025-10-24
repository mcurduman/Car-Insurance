# app/policy_expiry_worker.py
import asyncio
from datetime import datetime, time, timedelta, date
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import get_settings
from app.db.repositories.policy_repository import PolicyRepository
from app.service import policy_service
from app.utils.logging_utils import log_info, log_event
from app.db.session import AsyncSessionLocal # dacă e greu de folosit în worker, instanțiază repo direct

settings = get_settings()
TIMEZONE = getattr(settings, "TIMEZONE", "Europe/Bucharest")
JOB_INTERVAL_MINUTES = int(getattr(settings, "JOB_INTERVAL_MINUTES", 10))
WINDOW_MINUTES = int(getattr(settings, "WINDOW_MINUTES", 180))  # 3h = 180min

def now_tz() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE))

async def check_policy_expiry():
    now = now_tz()
    today = now.date()
    window_start = datetime.combine(today, time(5, 0), tzinfo=ZoneInfo(TIMEZONE))
    window_end = window_start.replace(hour=0, minute=0) + timedelta(minutes=WINDOW_MINUTES)

    log_info("policy_expiry_tick", ts=now.isoformat(), interval_min=JOB_INTERVAL_MINUTES)

    # rulează doar în fereastra [00:00, 01:00)
    if not (window_start <= now < window_end):
        log_info("policy_expiry_skipped_outside_window", now=now.isoformat(), window=f"[{window_start.isoformat()}, {window_end.isoformat()})")
        return
    
    log_info("policy_expiry_log_started_checking", timestamp=now.isoformat())

    async with AsyncSessionLocal() as session:
        repo = PolicyRepository(session)
        # IMPORTANT: conform specificitației task-ului e „end_date == today AND not yet logged”
        policies = await repo.get_policies_not_logged_expiry(today)

        if not policies:
            log_info("policy_expiry_no_items", date=str(today))
            return

        for p in policies:
            log_info("policy_expiry_processing", policy_id=p.id, car_id=p.car_id, end_date=str(p.end_date))
            p.logged_expiry_at = today  
            await repo.update_policy_logged_expiry(p.id, p.logged_expiry_at)
            log_info("policy_expiry_logged", policy_id=p.id, logged_at=now.isoformat())

async def main():
    log_info("policy_expiry_worker_starting", tz=TIMEZONE, interval_min=JOB_INTERVAL_MINUTES)

    scheduler = AsyncIOScheduler(timezone=ZoneInfo(TIMEZONE))
    scheduler.add_job(
        check_policy_expiry,
        trigger=IntervalTrigger(minutes=JOB_INTERVAL_MINUTES),
        id="policy_expiry_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
    )
    scheduler.start()
    log_info("policy_expiry_worker_started")

    # ȚINE PROCESUL ÎN VIAȚĂ
    await asyncio.Event().wait()

if __name__ == "__main__":
    import structlog
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        structlog.get_logger().info("policy_expiry_worker_stopped_by_signal")
