from app.db.repositories.policy_repository import PolicyRepository
from app.db.models.policy_model import InsurancePolicy

class PolicyService:
    def __init__(self, policy_repository: PolicyRepository):
        self.policy_repository = policy_repository

    async def get_policy(self, id: int) -> InsurancePolicy | None:
        return await self.policy_repository.get(id)

    async def get_policies_by_car_id(self, car_id: int) -> list[InsurancePolicy]:
        return await self.policy_repository.get_policies_by_car_id(car_id)

    async def add_policy(self, policy: InsurancePolicy) -> InsurancePolicy:
        return await self.policy_repository.add(policy)
    
    async def update_policy(self, policy: InsurancePolicy) -> InsurancePolicy:
        existing_policy = await self.policy_repository.get(policy.id)
        if not existing_policy:
            raise ValueError(f"Policy with ID {policy.id} does not exist.")
        return await self.policy_repository.update(policy)
    
    async def list_policies(self) -> list[InsurancePolicy]:
        return list(await self.policy_repository.list())