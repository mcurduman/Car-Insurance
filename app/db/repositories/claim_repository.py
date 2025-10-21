from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Iterable
from app.db.models.claim_model import Claim
from app.db.repositories.base_repository import BaseRepository

class ClaimRepository(BaseRepository[Claim, int]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Claim]:
        result = await self.session.execute(select(Claim).where(Claim.id == id))
        return result.scalars().first()

    async def get_by_car_id(self, car_id: int) -> Iterable[Claim]:
        result = await self.session.execute(select(Claim).where(Claim.car_id == car_id))
        return result.scalars().all()

    async def get_by_owner_id(self, owner_id: int) -> Iterable[Claim]:
        result = await self.session.execute(select(Claim).where(Claim.owner_id == owner_id))
        return result.scalars().all()

    async def add(self, entity: Claim) -> Claim:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def list(self) -> Iterable[Claim]:
        result = await self.session.execute(select(Claim))
        return result.scalars().all()

    async def delete(self, id: int) -> None:
        result = await self.session.execute(select(Claim).where(Claim.id == id))
        claim = result.scalars().first()
        if claim:
            await self.session.delete(claim)
            await self.session.commit()

    async def update(self, entity: Claim) -> Claim:
        await self.session.merge(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity