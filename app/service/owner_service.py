from app.db.repositories.owner_repository import OwnerRepository
from app.db.models.owner_model import Owner

class OwnerService:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    async def get_owner(self, id: int) -> Owner | None:
        return await self.owner_repository.get(id)
    
    async def add_owner(self, owner: Owner) -> Owner:
        return await self.owner_repository.add(owner)
    
    async def update_owner(self, owner: Owner) -> Owner:
        existing_owner = await self.owner_repository.get(owner.id)
        if not existing_owner:
            raise ValueError(f"Owner with ID {owner.id} does not exist.")
        return await self.owner_repository.update(owner)
    
    async def list_owners(self) -> list[Owner]:
        return list(await self.owner_repository.list())