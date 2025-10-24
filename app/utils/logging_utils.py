# logging_utils.py
import time
import functools
import inspect
import structlog
from app.core.logging import logger

log = logger

def log_event(event: str, level: str = "info", include_args: bool = False):
    """
    Loghează <event>_started / <event>_completed / <event>_failed + duration.
    include_args=False (default) ca să evităm PII în loguri.
    """
    def decorate(func):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def aw(*args, **kwargs):
                start = time.perf_counter()
                if include_args:
                    log.info(f"{event}_started", args=args, kwargs=kwargs)
                else:
                    log.info(f"{event}_started")
                try:
                    result = await func(*args, **kwargs)
                    dur = round(time.perf_counter() - start, 3)
                    getattr(log, level.lower())(f"{event}_completed", duration=dur)
                    return result
                except Exception as exc:
                    dur = round(time.perf_counter() - start, 3)
                    log.error(f"{event}_failed", error=str(exc), duration=dur, exc_info=True)
                    raise
            return aw
        else:
            @functools.wraps(func)
            def w(*args, **kwargs):
                start = time.perf_counter()
                if include_args:
                    log.info(f"{event}_started", args=args, kwargs=kwargs)
                else:
                    log.info(f"{event}_started")
                try:
                    result = func(*args, **kwargs)
                    dur = round(time.perf_counter() - start, 3)
                    getattr(log, level.lower())(f"{event}_completed", duration=dur)
                    return result
                except Exception as exc:
                    dur = round(time.perf_counter() - start, 3)
                    log.error(f"{event}_failed", error=str(exc), duration=dur, exc_info=True)
                    raise
            return w
    return decorate

def log_info(message: str, **kwargs):
    log.info(message, **kwargs)
