# app/core/logging.py
from __future__ import annotations
import logging, sys
from datetime import date, datetime
from decimal import Decimal
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
import structlog
from structlog.contextvars import merge_contextvars, bind_contextvars, clear_contextvars
from structlog.processors import TimeStamper
from structlog.stdlib import ProcessorFormatter, BoundLogger, LoggerFactory
from app.core.config import get_settings, Env

def get_logger() -> BoundLogger:
    return structlog.get_logger()

def bind_request_context(*, request_id: str | None = None, path: str | None = None,
                         method: str | None = None, **extra: Any) -> None:
    kv: Dict[str, Any] = {}
    if request_id:
        kv["request_id"] = request_id
    if path:
        kv["path"] = path
    if method:
        kv["method"] = method
    kv.update(extra or {})
    if kv:
        bind_contextvars(**kv)

def clear_request_context() -> None:
    clear_contextvars()

def _to_serializable(_: Any, __: Any, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    def conv(v: Any) -> Any:
        if isinstance(v, (datetime, date)):
            return v.isoformat()
        if isinstance(v, Decimal):
            try:
                return float(v)
            except Exception:
                return str(v)
        return v
    for k, v in list(event_dict.items()):
        event_dict[k] = conv(v)
    return event_dict

_CONFIGURED = False

def configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()
    is_dev = settings.ENV == Env.development
    log_level_name = (settings.LOG_LEVEL or ("DEBUG" if is_dev else "INFO")).upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    log_file_path = getattr(settings, "LOG_FILE_PATH", "logs/app.log")
    from pathlib import Path
    Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)

    logging.captureWarnings(True)
    renderer = structlog.dev.ConsoleRenderer() if is_dev else structlog.processors.JSONRenderer()
    formatter = ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=[
            merge_contextvars,
            structlog.processors.add_log_level,
            TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _to_serializable,
        ],
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logging.basicConfig(handlers=[stream_handler, file_handler], level=log_level, force=True)
    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.processors.add_log_level,
            TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _to_serializable,
            ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    for name in ("apscheduler"):
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.propagate = True

    _CONFIGURED = True

configure_logging()
logger = get_logger()