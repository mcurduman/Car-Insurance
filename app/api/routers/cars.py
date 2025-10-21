from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_async_session  # trebuie să returneze AsyncSession
from app.db.models.car_model import Car
from app.db.repositories.car_repository import CarRepository
from app.service.car_service import CarService
from app.schemas.car_schema import CarWithOwnerResponse, CarCreate, CarUpdate, CarResponse
from app.auth.oauth2 import get_current_user
from fastapi import Response
from app.schemas.claim_schema import ClaimCreate, ClaimResponse
from app.service.claim_service import ClaimService
from app.db.repositories.claim_repository import ClaimRepository
from app.db.models.claim_model import Claim

router = APIRouter(prefix="/api/cars", tags=["cars"], dependencies=[Depends(get_current_user)])
async def get_car_service(
    session: AsyncSession = Depends(get_async_session),
) -> CarService:
    car_repository = CarRepository(session)
    return CarService(car_repository)

async def get_claim_service(session: AsyncSession = Depends(get_async_session)) -> ClaimService:
    claim_repository = ClaimRepository(session)
    return ClaimService(claim_repository)

@router.get("/", response_model=List[CarWithOwnerResponse])
async def list_cars(service: CarService = Depends(get_car_service)):
    cars = await service.list_cars_with_owner()
    return cars

@router.get("/{car_id}", response_model=CarResponse)
async def get_car(car_id: int, service: CarService = Depends(get_car_service)):
    car = await service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@router.post("/{car_id}/claims/")
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
    # Validate claimCreate fields (Pydantic already does most)
    claim = Claim(
        car_id=car_id,
        claim_date=claim_create.claim_date,
        description=claim_create.description,
        amount=claim_create.amount
    )
    new_claim = await claim_service.add_claim(claim)
    response.headers["Location"] = f"/api/cars/{car_id}/claims/{new_claim.id}"
    return new_claim

@router.get("/by-vin/{vin}", response_model=CarResponse)
async def get_car_by_vin(vin: str, service: CarService = Depends(get_car_service)):
    car = await service.get_car_by_vin(vin)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    car_create: CarCreate,
    service: CarService = Depends(get_car_service),
):
    car = Car(**car_create.model_dump())
    try:
        new_car = await service.add_car(car)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_car

@router.put("/{car_id}", response_model=CarResponse)
async def update_car(
    car_id: int,
    car_update: CarUpdate,
    service: CarService = Depends(get_car_service),
):
    existing_car = await service.get_car(car_id)
    if not existing_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    update_data = car_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_car, key, value)

    try:
        updated_car = await service.update_car(existing_car)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated_car

@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: int,
    service: CarService = Depends(get_car_service),
):
    existing_car = await service.get_car(car_id)
    if not existing_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    await service.car_repository.delete(car_id)


