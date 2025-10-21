from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_session  # trebuie să returneze AsyncSession
from app.db.models.claim_model import Claim
from app.db.repositories.claim_repository import ClaimRepository
from app.service.claim_service import ClaimService
from app.schemas.claim_schema import ClaimBase, ClaimCreate, ClaimUpdate, ClaimResponse

router = APIRouter(prefix="/claims", tags=["claims"])
async def get_claim_service(
    session: AsyncSession = Depends(get_async_session),
) -> ClaimService:
    claim_repository = ClaimRepository(session)
    return ClaimService(claim_repository)

@router.get("/", response_model=List[ClaimResponse])
async def list_claims(service: ClaimService = Depends(get_claim_service)):
    claims = await service.list_claims()
    return claims

@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(claim_id: int, service: ClaimService = Depends(get_claim_service
)):
    claim = await service.get_claim(claim_id)
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    return claim

@router.post("/", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_create: ClaimCreate,
    service: ClaimService = Depends(get_claim_service),
):
    claim = Claim(**claim_create.model_dump())
    try:
        new_claim = await service.add_claim(claim)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_claim

@router.put("/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    claim_id: int,
    claim_update: ClaimUpdate,
    service: ClaimService = Depends(get_claim_service),
):
    existing_claim = await service.get_claim(claim_id)
    if not existing_claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    update_data = claim_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_claim, field, value)

    try:
        updated_claim = await service.update_claim(existing_claim)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated_claim

@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(
    claim_id: int,
    service: ClaimService = Depends(get_claim_service),
):
    existing_claim = await service.get_claim(claim_id)
    if not existing_claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    await service.delete_claim(claim_id)
    return None

