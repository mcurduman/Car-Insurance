import structlog
log = structlog.get_logger()

def policy_created(policy_id: str, customer_id: str, product: str):
    log.info("policy_created", policy_id=policy_id, customer_id=customer_id, product=product)

def policy_updated(policy_id: str, changes: dict):
    log.info("policy_updated", policy_id=policy_id, changes=changes)

def claim_created(claim_id: str, policy_id: str, amount: float, currency: str = "EUR"):
    log.info("claim_created", claim_id=claim_id, policy_id=policy_id, amount=amount, currency=currency)

def policy_expiry_detected(policy_id: str, expires_at: str, source: str = "task_d"):
    log.info("policy_expiry_detected", policy_id=policy_id, expires_at=expires_at, source=source)
