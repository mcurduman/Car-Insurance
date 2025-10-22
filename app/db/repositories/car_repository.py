from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Iterable
from app.db.models.car_model import Car
from app.db.repositories.base_repository import BaseRepository
from sqlalchemy.orm import joinedload

class CarRepository(BaseRepository[Car, int]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Car]:
        result = await self.session.execute(select(Car).where(Car.id == id))
        scalars_result = result.scalars()
        return scalars_result.first()
    
    async def get_car_by_vin(self, vin: str) -> Optional[Car]:
        result = await self.session.execute(select(Car).where(Car.vin == vin))
        scalars_result = result.scalars()
        return scalars_result.first()

    async def add(self, entity: Car) -> Car:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def list(self) -> Iterable[Car]:
        result = await self.session.execute(select(Car))
        scalars_result = result.scalars()
        return scalars_result.all()
    
    async def list_with_owner(self) -> Iterable[Car]:
        result = await self.session.execute(select(Car).options(joinedload(Car.owner)))
        scalars_result = result.scalars()
        return scalars_result.all()

    async def delete(self, id: int) -> None:
        result = await self.session.execute(select(Car).where(Car.id == id))
        scalars_result = result.scalars()
        car = scalars_result.first()
        if car:
            await self.session.delete(car)
            await self.session.commit()

    async def update(self, entity: Car) -> Car:
        await self.session.merge(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
