from fastapi import FastAPI
import logging
from app.core.config import get_settings
from app.core import middleware
from app.api.routers import cars, owners, claims, health, policies, auth, history
from fastapi.middleware.cors import CORSMiddleware

cfg = get_settings()
app = FastAPI(title=cfg.APP_NAME, debug=(cfg.ENV == "development"))
app.add_middleware(middleware.RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cars.router)
app.include_router(owners.router)
app.include_router(health.router)
app.include_router(claims.router)
app.include_router(policies.router)
app.include_router(history.router)
app.include_router(auth.router)

logging.basicConfig(level=getattr(logging, cfg.LOG_LEVEL),
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")