from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.oauth2 import get_current_user
from app.db.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_session  # trebuie să returneze AsyncSession
from app.db.models.owner_model import Owner
from app.db.repositories.owner_repository import OwnerRepository
from app.service.owner_service import OwnerService
from app.schemas.owner_schema import OwnerCreate, OwnerUpdate, OwnerResponse

router = APIRouter(prefix="/owners", tags=["owners"], dependencies=[Depends(get_current_user)])
async def get_owner_service(
    session: AsyncSession = Depends(get_async_session),
) -> OwnerService:
    owner_repository = OwnerRepository(session)
    return OwnerService(owner_repository)

@router.get("/", response_model=List[OwnerResponse])
async def list_owners(service: OwnerService = Depends(get_owner_service)):
    owners = await service.list_owners()
    return owners

@router.get("/{owner_id}", response_model=OwnerResponse)
async def get_owner(owner_id: int, service: OwnerService = Depends(get_owner_service)):
    owner = await service.get_owner(owner_id)
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return owner

@router.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_owner(
    owner_create: OwnerCreate,
    service: OwnerService = Depends(get_owner_service),
):
    owner = Owner(**owner_create.model_dump())
    try:
        new_owner = await service.add_owner(owner)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_owner

@router.put("/{owner_id}", response_model=OwnerResponse)
async def update_owner(
    owner_id: int,
    owner_update: OwnerUpdate,
    service: OwnerService = Depends(get_owner_service),
):
    existing_owner = await service.get_owner(owner_id)
    if not existing_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")

    update_data = owner_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_owner, field, value)

    try:
        updated_owner = await service.update_owner(existing_owner)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated_owner



