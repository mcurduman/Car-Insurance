from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.auth.oauth2 import get_current_user
from app.api.deps import get_car_service, get_policy_service, get_validity_service
from app.db.models.policy_model import InsurancePolicy
from app.service.policy_service import PolicyService
from app.schemas.policy_schema import InsurancePolicyCreate, InsurancePolicyResponse
from app.service.car_service import CarService
from app.utils.events import policy_created
from app.utils.logging_utils import log_event


router = APIRouter(prefix="/api/cars", tags=["policies"], dependencies=[Depends(get_current_user)])

@router.post("/{car_id}/policies/", status_code=status.HTTP_201_CREATED)
@log_event("create_policy_for_car")
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
    policy_created(
        policy_id=new_policy.id,
        car_id=new_policy.car_id,
        provider=new_policy.provider,
        start_date=new_policy.start_date,
        end_date=new_policy.end_date
    )
    return new_policy

@router.get("/{car_id}/policies/{policy_id}", response_model=InsurancePolicyResponse)
@log_event("get_policy_for_car")
async def get_policy_for_car(car_id: int, policy_id: int, policy_service: PolicyService = Depends(get_policy_service)):
    policy = await policy_service.get_policy(policy_id)
    if not policy or policy.car_id != car_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found for this car")
    return policy

@router.get("/{car_id}/policies", response_model=List[InsurancePolicyResponse])
@log_event("list_policies_for_car")
async def list_policies_for_car(
    car_id: int,
    policy_service: PolicyService = Depends(get_policy_service)
):
    policies = await policy_service.get_policies_by_car_id(car_id)
    return policies

@router.get("/policies/", response_model=List[InsurancePolicyResponse])
@log_event("get_policies")
async def get_policies(policy_service: PolicyService = Depends(get_policy_service)):
    return await policy_service.list_policies()

@router.delete("/{car_id}/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_event("delete_policy_for_car")
async def delete_policy_for_car(
    car_id: int,
    policy_id: int,
    policy_service: PolicyService = Depends(get_policy_service)
):
    policy = await policy_service.get_policy(policy_id)
    if not policy or policy.car_id != car_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found for this car")
    await policy_service.delete_policy(policy_id)


@router.get("/{car_id}/insurance-valid")
@log_event("check_insurance_validity_for_car")
async def check_insurance_validity_for_car(
    car_id: int,
    date: date,
    policy_service: PolicyService = Depends(get_policy_service),
    car_service: CarService = Depends(get_car_service)
):
    car = await car_service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    # Accept only dates between 1900-01-01 and 2100-12-31
    if not (date(1900, 1, 1) <= date <= date(2100, 12, 31)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date must be between 1900-01-01 and 2100-12-31"
        )
    is_valid = await policy_service.is_active_policy_exists_for_car(car_id, date)
    return {"car_id": car_id, "date": date.isoformat(), "valid": is_valid}