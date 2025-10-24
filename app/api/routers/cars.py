from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_car_service, get_validity_service # trebuie să returneze AsyncSession
from app.db.models.car_model import Car
from app.service.car_service import CarService
from app.schemas.car_schema import CarWithOwnerResponse, CarCreate, CarUpdate, CarResponse
from app.auth.oauth2 import get_current_user
from fastapi import Response
from app.service.validity_service import ValidityService
from datetime import date
from app.utils.logging_utils import log_event

router = APIRouter(prefix="/api/cars", tags=["cars"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=List[CarWithOwnerResponse])
@log_event("list_cars")
async def list_cars(service: CarService = Depends(get_car_service)):
    cars = await service.list_cars_with_owner()
    return cars

@router.get("/{car_id}", response_model=CarResponse)
@log_event("get_car")
async def get_car(car_id: int, service: CarService = Depends(get_car_service)):
    car = await service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@router.get("/{car_id}/insurance-valid", response_model=dict)
@log_event("check_insurance_validity")
async def insurance_valid(
    car_id: int,
    date: date,
    car_service: CarService = Depends(get_car_service),
    validity_service: ValidityService = Depends(get_validity_service)
):
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    #
    if date.year < 1900 or date.year > 2100:
        raise HTTPException(status_code=400, detail="Invalid date format or out of range (1900-2100)")
    valid = await validity_service.is_valid(car_id, date)
    return {"carId": car_id, "date": date, "valid": valid}

@router.get("/by-vin/{vin}", response_model=CarResponse)
@log_event("get_car_by_vin")
async def get_car_by_vin(vin: str, service: CarService = Depends(get_car_service)):
    car = await service.get_car_by_vin(vin)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
@log_event("create_car")
async def create_car(
    car_create: CarCreate,
    response: Response,
    service: CarService = Depends(get_car_service),
):
    car = Car(**car_create.model_dump())
    try:
        new_car = await service.add_car(car)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    response.headers["Location"] = f"/api/cars/{new_car.id}"
    return new_car

@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_event("delete_car")
async def delete_car(
    car_id: int,
    service: CarService = Depends(get_car_service),
):
    existing_car = await service.get_car(car_id)
    if not existing_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    await service.car_repository.delete(car_id)


