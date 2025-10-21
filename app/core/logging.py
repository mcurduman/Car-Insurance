# logging_setup.py
import os
import sys
import logging
import structlog
from structlog.processors import TimeStamper
from structlog.contextvars import merge_contextvars

ENV = os.getenv("ENV", "development")  # "development" | "production"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if ENV == "development" else "INFO").upper()

def configure_logging():
    # Scriem pe stdout (bun pentru Docker + fluent-bit/Loki/ELK)
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    processors = [
        merge_contextvars,                        # include contextvars (ex: request_id)
        structlog.processors.add_log_level,
        TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # JSON în production, human-readable în development
    renderer = (
        structlog.processors.JSONRenderer()
        if ENV == "production"
        else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[*processors, renderer],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()

logger = configure_logging()
