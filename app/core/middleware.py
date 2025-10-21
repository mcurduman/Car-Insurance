# middleware.py
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars

REQUEST_ID_HEADER = "x-request-id"

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get(REQUEST_ID_HEADER, str(uuid.uuid4()))
        bind_contextvars(request_id=rid, path=str(request.url.path), method=request.method)
        try:
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = rid
            return response
        finally:
            clear_contextvars()
