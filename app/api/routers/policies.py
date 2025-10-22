from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.auth.oauth2 import get_current_user
from app.api.deps import get_car_service, get_policy_service
from app.db.models.policy_model import InsurancePolicy
from app.service.policy_service import PolicyService
from app.schemas.policy_schema import InsurancePolicyCreate, InsurancePolicyResponse
from app.service.car_service import CarService


router = APIRouter(prefix="/api/cars", tags=["policies"], dependencies=[Depends(get_current_user)])

@router.post("/{car_id}/policies/", status_code=status.HTTP_201_CREATED)
async def create_policy_for_car(
    car_id: int,
    policy_create: InsurancePolicyCreate,
    response: Response,
    car_service: CarService = Depends(get_car_service),
    policy_service: PolicyService = Depends(get_policy_service),
):
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    policy = InsurancePolicy(**policy_create.model_dump())
    new_policy = await policy_service.add_policy(policy)
    response.headers["Location"] = f"/api/cars/{car_id}/policies/{new_policy.id}"
    return new_policy

@router.get("/{car_id}/policies/{policy_id}", response_model=InsurancePolicyResponse)
async def get_policy_for_car(car_id: int, policy_id: int, policy_service: PolicyService = Depends(get_policy_service)):
    policy = await policy_service.get_policy(policy_id)
    if not policy or policy.car_id != car_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found for this car")
    return policy

@router.get("/{car_id}/policies", response_model=List[InsurancePolicyResponse])
async def list_policies_for_car(
    car_id: int,
    policy_service: PolicyService = Depends(get_policy_service)
):
    policies = await policy_service.get_policies_by_car_id(car_id)
    return policies