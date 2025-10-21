from app.db.repositories.car_repository import CarRepository
from app.db.models.car_model import Car
from app.db.repositories.policy_repository import PolicyRepository
from app.db.repositories.claim_repository import ClaimRepository

class CarService:
    def __init__(self, car_repository: CarRepository):
        self.car_repository = car_repository

    async def get_car(self, id: int) -> Car | None:
        return await self.car_repository.get(id)
    
    async def get_car_by_vin(self, vin: str) -> Car | None:
        return await self.car_repository.get_car_by_vin(vin)
    
    async def add_car(self, car: Car) -> Car:
        existing_car = await self.car_repository.get_car_by_vin(car.vin)
        if existing_car:
            raise ValueError(f"Car with VIN {car.vin} already exists.")

        return await self.car_repository.add(car)
    
    async def update_car(self, car: Car) -> Car:
        existing_car = await self.car_repository.get(car.id)
        if not existing_car:
            raise ValueError(f"Car with ID {car.id} does not exist.")
        if car.vin != existing_car.vin:
            raise ValueError("VIN cannot be changed.")
        return await self.car_repository.update(car)
    
    async def list_cars(self) -> list[Car]:
        return list(await self.car_repository.list())
    
    async def list_cars_with_owner(self) -> list[Car]:
        return list(await self.car_repository.list_with_owner())

    
    async def delete_car(self, id: int) -> None:
        car = await self.car_repository.get(id)
        if not car:
            raise ValueError(f"Car with ID {id} does not exist.")
        await self.car_repository.delete(id)
        