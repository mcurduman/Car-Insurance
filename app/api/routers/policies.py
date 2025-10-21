from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_session  # trebuie să returneze AsyncSession
from app.db.models.policy_model import InsurancePolicy
from app.db.repositories.policy_repository import PolicyRepository
from app.service.policy_service import PolicyService
from app.schemas.policy_schema import InsurancePolicyBase, InsurancePolicyCreate, InsurancePolicyUpdate, InsurancePolicyResponse

router = APIRouter(prefix="/policies", tags=["policies"])

async def get_policy_service(
    session: AsyncSession = Depends(get_async_session),
) -> PolicyService:
    policy_repository = PolicyRepository(session)
    return PolicyService(policy_repository)

@router.get("/", response_model=List[InsurancePolicyResponse])
async def list_policies(service: PolicyService = Depends(get_policy_service)):
    policies = await service.list_policies()
    return policies

@router.get("/{policy_id}", response_model=InsurancePolicyResponse)
async def get_policy(policy_id: int, service: PolicyService = Depends(get_policy_service)):
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy

@router.post("/", response_model=InsurancePolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_create: InsurancePolicyCreate,
    service: PolicyService = Depends(get_policy_service),
):
    policy = InsurancePolicy(**policy_create.model_dump())
    try:
        new_policy = await service.add_policy(policy)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_policy

@router.put("/{policy_id}", response_model=InsurancePolicyResponse)
async def update_policy(
    policy_id: int,
    policy_update: InsurancePolicyUpdate,
    service: PolicyService = Depends(get_policy_service),
):
    existing_policy = await service.get_policy(policy_id)
    if not existing_policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    update_data = policy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_policy, field, value)

    try:
        updated_policy = await service.update_policy(existing_policy)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated_policy

@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(policy_id: int, service: PolicyService = Depends(get_policy_service)):
    existing_policy = await service.get_policy(policy_id)
    if not existing_policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    await service.delete_policy(policy_id)
