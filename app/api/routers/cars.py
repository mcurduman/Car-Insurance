from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_session  # trebuie să returneze AsyncSession
from app.db.models.car_model import Car
from app.db.repositories.car_repository import CarRepository
from app.service.car_service import CarService
from app.schemas.car_schema import CarBase, CarCreate, CarUpdate, CarResponse


router = APIRouter(prefix="/cars", tags=["cars"])
async def get_car_service(
    session: AsyncSession = Depends(get_async_session),
) -> CarService:
    car_repository = CarRepository(session)
    return CarService(car_repository)

@router.get("/", response_model=List[CarResponse])
async def list_cars(service: CarService = Depends(get_car_service)):
    cars = await service.list_cars()
    return cars

@router.get("/{car_id}", response_model=CarResponse)
async def get_car(car_id: int, service: CarService = Depends(get_car_service)):
    car = await service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

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


