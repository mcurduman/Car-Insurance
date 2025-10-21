from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import get_settings

cfg = get_settings()
engine = create_async_engine(
    cfg.DATABASE_URL,               # sqlite+aiosqlite (dev) sau postgresql+asyncpg (prod)
    future=True,
    pool_pre_ping=True,
    echo=(cfg.LOG_LEVEL=="DEBUG"),
)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)