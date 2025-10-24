from fastapi import APIRouter, status
from app.utils.logging_utils import log_event

router = APIRouter(tags=["health"])

@router.get("/health", response_model=dict, status_code=status.HTTP_200_OK)

async def health_status():
    return {"status": "ok"}
