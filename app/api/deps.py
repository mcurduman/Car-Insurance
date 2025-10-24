from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from fastapi import Depends
from app.service.validity_service import ValidityService
from app.db.repositories.car_repository import CarRepository
from app.service.car_service import CarService
from app.db.repositories.policy_repository import PolicyRepository
from app.service.policy_service import PolicyService
from app.db.repositories.claim_repository import ClaimRepository
from app.service.claim_service import ClaimService
from app.db.repositories.owner_repository import OwnerRepository
from app.service.owner_service import OwnerService
from app.db.repositories.user_repository import UserRepository
from app.service.user_service import UserService

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as s:
        yield s

async def get_car_service(
    session: AsyncSession = Depends(get_async_session),
):
    car_repository = CarRepository(session)
    return CarService(car_repository)

async def get_policy_service(
    session: AsyncSession = Depends(get_async_session),
):
    policy_repository = PolicyRepository(session)
    return PolicyService(policy_repository)

async def get_claim_service(
    session: AsyncSession = Depends(get_async_session),
):
    claim_repository = ClaimRepository(session)
    return ClaimService(claim_repository)

async def get_owner_service(
    session: AsyncSession = Depends(get_async_session),
):
    owner_repository = OwnerRepository(session)
    return OwnerService(owner_repository)

async def get_validity_service(
    session: AsyncSession = Depends(get_async_session),
):
    
    return ValidityService(session)

async def get_history_service(
    session: AsyncSession = Depends(get_async_session),
):
    from app.service.history_service import HistoryService
    return HistoryService(session)

async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
):
    user_repository = UserRepository(session)
    return UserService(user_repository)