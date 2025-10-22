from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import User, UserCreate
from app.service import user_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwt import create_access_token
from app.core.security import verify_password
from app.api.deps import get_async_session
from app.db.repositories.user_repository import UserRepository
from app.service.user_service import UserService
from fastapi import status

router = APIRouter(tags=["auth"])
async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: user_service.UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_service: user_service.UserService = Depends(get_user_service)):
    return await user_service.create_user(user)
