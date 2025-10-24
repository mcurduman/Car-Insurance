import structlog
log = structlog.get_logger()

def policy_created(policy_id: int, car_id: int, provider: str, start_date, end_date):
    log.info("policy_created", policy_id=policy_id, car_id=car_id, provider=provider, start_date=start_date, end_date=end_date)

def policy_updated(policy_id: int, car_id: int = None, provider: str = None, start_date=None, end_date=None, changes: dict = None):
    log.info("policy_updated", policy_id=policy_id, car_id=car_id, provider=provider, start_date=start_date, end_date=end_date, changes=changes)

def claim_created(claim_id: int, amount: float, car_id: int):
    log.info("claim_created", claim_id=claim_id, amount=amount, car_id=car_id)

def policy_expiry_detected(policy_id: int, car_id: int, provider: str, start_date, end_date, expires_at: str, source: str = "task_d"):
    log.info("policy_expiry_detected", policy_id=policy_id, car_id=car_id, provider=provider, start_date=start_date, end_date=end_date, expires_at=expires_at, source=source)
