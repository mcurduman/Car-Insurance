from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Iterable
from app.db.models.policy_model import InsurancePolicy
from app.db.repositories.base_repository import BaseRepository
from datetime import date

class PolicyRepository(BaseRepository[InsurancePolicy, int]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[InsurancePolicy]:
        result = await self.session.execute(select(InsurancePolicy).where(InsurancePolicy.id == id))
        return result.scalars().first()

    async def get_policies_by_car_id(self, car_id: int) -> list[InsurancePolicy]:
        result = await self.session.execute(select(InsurancePolicy).where(InsurancePolicy.car_id == car_id))
        return result.scalars().all()
    
    async def is_active_policy_exists_for_car(self, car_id: int, on_date: date) -> bool:
        result = await self.session.execute(
            select(InsurancePolicy).where(
                InsurancePolicy.car_id == car_id,
                InsurancePolicy.start_date <= on_date,
                InsurancePolicy.end_date >= on_date,
                InsurancePolicy.logged_expiry_at == None
            )
        )
        policy = result.scalars().first()
        return policy is not None

    async def get_policies_not_logged_expiry(self, before_date) -> list[InsurancePolicy]:
        result = await self.session.execute(
            select(InsurancePolicy).where(
                InsurancePolicy.end_date < before_date,
                InsurancePolicy.logged_expiry_at == None
            )
        )
        return result.scalars().all()
    
    async def update_policy_logged_expiry(self, policy_id: int, logged_expiry_at: date):
        result = await self.session.execute(select(InsurancePolicy).where(InsurancePolicy.id == policy_id))
        policy = result.scalars().first()
        if policy:
            policy.logged_expiry_at = logged_expiry_at
            await self.session.commit()
            await self.session.refresh(policy)
            return policy
        return None
    
    
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
