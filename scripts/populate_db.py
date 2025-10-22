import asyncio
import json
from app.api.deps import get_async_session
from app.db.models.owner_model import Owner
from app.db.models.car_model import Car
from app.db.models.policy_model import InsurancePolicy
from app.db.models.claim_model import Claim
from sqlalchemy import select
from datetime import date, datetime

FAKE_OWNERS_FILE = "scripts/fake_owners.json"
FAKE_CARS_FILE = "scripts/fake_cars.json"
FAKE_POLICIES_FILE = "scripts/fake_policies.json"
FAKE_CLAIMS_FILE = "scripts/fake_claims.json"


async def populate():
    # Load fake owners
    with open(FAKE_OWNERS_FILE, "r") as f:
        owners_data = json.load(f)
    # Load fake cars
    with open(FAKE_CARS_FILE, "r") as f:
        cars_data = json.load(f)
    # Load fake policies
    with open(FAKE_POLICIES_FILE, "r") as f:
        policies_data = json.load(f)
    # Load fake claims
    with open(FAKE_CLAIMS_FILE, "r") as f:
        claims_data = json.load(f)

    async for session in get_async_session():
        # Owners
        owner_objs = []
        for owner_data in owners_data:
            result = await session.execute(select(Owner).where(Owner.email == owner_data["email"]))
            owner = result.scalars().first()
            if not owner:
                owner = Owner(**owner_data)
                session.add(owner)
                await session.flush()
            owner_objs.append(owner)
        await session.commit()

        # Cars
        car_objs = []
        for i, car_data in enumerate(cars_data):
            result = await session.execute(select(Car).where(Car.vin == car_data["vin"]))
            car = result.scalars().first()
            if not car:
                # Assign owner_id round-robin
                car = Car(**car_data, owner_id=owner_objs[i % len(owner_objs)].id)
                session.add(car)
                await session.flush()
            car_objs.append(car)
        await session.commit()

        # Policies
        policy_objs = []
        for i, policy_data in enumerate(policies_data):
            # Convert dates from string to date
            start_date = datetime.fromisoformat(policy_data["start_date"]).date()
            end_date = datetime.fromisoformat(policy_data["end_date"]).date()
            result = await session.execute(select(InsurancePolicy).where(InsurancePolicy.policy_number == policy_data["policy_number"]))
            policy = result.scalars().first()
            if not policy:
                # Assign car_id round-robin
                policy = InsurancePolicy(
                    policy_number=policy_data["policy_number"],
                    start_date=start_date,
                    end_date=end_date,
                    premium=policy_data["premium"],
                    status=policy_data["status"],
                    car_id=car_objs[i % len(car_objs)].id
                )
                session.add(policy)
                await session.flush()
            policy_objs.append(policy)
        await session.commit()

        # Claims
        for i, claim_data in enumerate(claims_data):
            claim_date = datetime.fromisoformat(claim_data["date"]).date()
            result = await session.execute(select(Claim).where(Claim.claim_number == claim_data["claim_number"]))
            claim = result.scalars().first()
            if not claim:
                claim = Claim(
                    claim_number=claim_data["claim_number"],
                    date=claim_date,
                    amount=claim_data["amount"],
                    status=claim_data["status"],
                    description=claim_data["description"],
                    car_id=car_objs[i % len(car_objs)].id
                )
                session.add(claim)
        await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(populate())
