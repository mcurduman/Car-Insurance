from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.oauth2 import get_current_user
from app.utils.events import claim_created
from app.utils.logging_utils import log_event
from fastapi import Response
from app.api.deps import get_car_service, get_claim_service
from app.service.car_service import CarService
from app.db.models.claim_model import Claim
from app.schemas.claim_schema import ClaimResponse
from app.service.claim_service import ClaimService
from app.schemas.claim_schema import ClaimCreate

router = APIRouter(prefix="/api/cars", tags=["claims"], dependencies=[Depends(get_current_user)])

@router.post("/{car_id}/claims/", status_code=status.HTTP_201_CREATED)
@log_event("create_claim_for_car")
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
    claim_created(
        claim_id=new_claim.id,
        car_id=new_claim.car_id,
        amount=new_claim.amount
    )
    return new_claim

@router.get("/{car_id}/claims/{claim_id}")
@log_event("get_claim_for_car")
async def get_claim_for_car(car_id: int, claim_id: int, claim_service: ClaimService = Depends(get_claim_service),
                            car_service: CarService = Depends(get_car_service)):
    
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    claim = await claim_service.get_claim(claim_id)
    if not claim or claim.car_id != car_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found for this car")
    return claim

@router.get("/claims/", response_model=List[ClaimResponse])
@log_event("get_claims")
async def get_claims(claim_service: ClaimService = Depends(get_claim_service)):
    return await claim_service.list_claims()

@router.get("/{car_id}/claims", response_model=List[ClaimResponse])
@log_event("list_claims_for_car")
async def list_claims_for_car(
    car_id: int,
    claim_service: ClaimService = Depends(get_claim_service)
):
    claims = await claim_service.get_claims_by_car_id(car_id)
    return claims

@router.delete("/{car_id}/claims/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_event("delete_claim_for_car")
async def delete_claim_for_car(
    car_id: int,
    claim_id: int,
    claim_service: ClaimService = Depends(get_claim_service),
    car_service: CarService = Depends(get_car_service)
):
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    claim = await claim_service.get_claim(claim_id)
    if not claim or claim.car_id != car_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found for this car")
    await claim_service.delete_claim(claim_id)