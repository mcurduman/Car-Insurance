from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.policy_repository import PolicyRepository
from app.db.repositories.car_repository import CarRepository
from app.db.repositories.claim_repository import ClaimRepository
from datetime import date

class HistoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_car_history(self, car_id: int):
        car_repo = CarRepository(self.session)
        policy_repo = PolicyRepository(self.session)
        claim_repo = ClaimRepository(self.session)
        car = await car_repo.get(car_id)
        if not car:
            return None
        policies = await policy_repo.get_policies_by_car_id(car_id)
        claims = await claim_repo.get_by_car_id(car_id)
        history = []
        for p in policies:
            history.append({
                "type": "POLICY",
                "policyId": p.id,
                "startDate": str(p.start_date),
                "endDate": str(p.end_date),
                "provider": p.provider
            })
        for c in claims:
            history.append({
                "type": "CLAIM",
                "claimId": c.id,
                "claimDate": str(c.claim_date),
                "amount": float(c.amount),
                "description": c.description
            })
            
        def get_sort_key(item):
            if item["type"] == "POLICY":
                return item["startDate"]
            else:
                return item["claimDate"]
        history.sort(key=get_sort_key)
        return history
        
