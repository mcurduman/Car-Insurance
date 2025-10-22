from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.oauth2 import get_current_user
from app.db.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.utils.events import claim_created
from app.utils.logging_utils import log_event
from fastapi import Response
from app.api.deps import get_async_session, get_car_service, get_claim_service
from app.service.car_service import CarService
from app.db.models.claim_model import Claim
from app.db.repositories.claim_repository import ClaimRepository
from app.service.claim_service import ClaimService
from app.schemas.claim_schema import ClaimCreate, ClaimUpdate, ClaimResponse

router = APIRouter(prefix="/api/cars", tags=["claims"], dependencies=[Depends(get_current_user)])

@router.post("/{car_id}/claims/", status_code=status.HTTP_201_CREATED)
async def create_claim_for_car(
    car_id: int,
    claim_create: ClaimCreate,
    response: Response,
    car_service: CarService = Depends(get_car_service),
    claim_service: ClaimService = Depends(get_claim_service),
):
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    claim = Claim(**claim_create.model_dump())
    new_claim = await claim_service.add_claim(claim)
    response.headers["Location"] = f"/api/cars/{car_id}/claims/{new_claim.id}"
    return new_claim

@router.get("/{car_id}/claims/{claim_id}")
async def get_claim_for_car(car_id: int, claim_id: int, claim_service: ClaimService = Depends(get_claim_service),
                            car_service: CarService = Depends(get_car_service)):
    
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    claim = await claim_service.get_claim(claim_id)
    if not claim or claim.car_id != car_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found for this car")
    return claim