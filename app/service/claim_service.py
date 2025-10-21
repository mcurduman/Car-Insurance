from app.db.repositories.claim_repository import ClaimRepository
from app.db.models.claim_model import Claim

class ClaimService:
    def __init__(self, claim_repository: ClaimRepository):
        self.claim_repository = claim_repository

    async def get_claim(self, id: int) -> Claim | None:
        return await self.claim_repository.get(id)
    
    async def get_claims_by_car_id(self, car_id: int) -> list[Claim]:
        return list(await self.claim_repository.get_by_car_id(car_id))
    
    async def get_claims_by_owner_id(self, owner_id: int) -> list[Claim]:
        return list(await self.claim_repository.get_by_owner_id(owner_id))
    
    async def add_claim(self, claim: Claim) -> Claim:
        return await self.claim_repository.add(claim)
    
    async def update_claim(self, claim: Claim) -> Claim:
        existing_claim = await self.claim_repository.get(claim.id)
        if not existing_claim:
            raise ValueError(f"Claim with ID {claim.id} does not exist.")
        return await self.claim_repository.update(claim)
    
    async def list_claims(self) -> list[Claim]:
        return list(await self.claim_repository.list())