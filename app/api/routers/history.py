
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_history_service
from app.auth.oauth2 import get_current_user
from typing import List
from app.utils.logging_utils import log_event

router = APIRouter(prefix="/api/cars", tags=["history"], dependencies=[Depends(get_current_user)]) 

@router.get("/{car_id}/history", response_model=List[dict], status_code=200)
@log_event("get_car_history")
async def get_car_history(
    car_id: int,
    history_service = Depends(get_history_service)
):
    history = await history_service.get_car_history(car_id)
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return history