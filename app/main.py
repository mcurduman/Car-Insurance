from fastapi import FastAPI
import logging
from app.core.config import get_settings
from app.api.routers import cars, owners, claims, health, policies

cfg = get_settings()
app = FastAPI(title=cfg.APP_NAME, debug=(cfg.ENV == "development"))
app.include_router(cars.router)
app.include_router(owners.router)
app.include_router(claims.router)
app.include_router(health.router)
app.include_router(policies.router)

logging.basicConfig(level=getattr(logging, cfg.LOG_LEVEL),
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")