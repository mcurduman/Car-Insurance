from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Iterable
from app.db.models.owner_model import Owner
from app.db.repositories.base_repository import BaseRepository

class OwnerRepository(BaseRepository[Owner, int]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[Owner]:
        result = await self.session.execute(select(Owner).where(Owner.id == id))
        return result.scalars().first()

    async def add(self, entity: Owner) -> Owner:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def list(self) -> Iterable[Owner]:
        result = await self.session.execute(select(Owner))
        return result.scalars().all()

    async def delete(self, id: int) -> None:
        result = await self.session.execute(select(Owner).where(Owner.id == id))
        owner = result.scalars().first()
        if owner:
            await self.session.delete(owner)
            await self.session.commit()

    async def update(self, entity: Owner) -> Owner:
        await self.session.merge(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity