from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Iterable
from app.db.models.policy_model import InsurancePolicy
from app.db.repositories.base_repository import BaseRepository

class PolicyRepository(BaseRepository[InsurancePolicy, int]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[InsurancePolicy]:
        result = await self.session.execute(select(InsurancePolicy).where(InsurancePolicy.id == id))
        return result.scalars().first()

    async def get_by_car_id(self, car_id: int) -> Optional[InsurancePolicy]:
        result = await self.session.execute(select(InsurancePolicy).where(InsurancePolicy.car_id == car_id))
        return result.scalars().first()

    async def add(self, entity: InsurancePolicy) -> InsurancePolicy:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def list(self) -> Iterable[InsurancePolicy]:
        result = await self.session.execute(select(InsurancePolicy))
        return result.scalars().all()
    
    async def delete(self, id: int) -> None:
        result = await self.session.execute(select(InsurancePolicy).where(InsurancePolicy.id == id))
        policy = result.scalars().first()
        if policy:
            await self.session.delete(policy)
            await self.session.commit()
