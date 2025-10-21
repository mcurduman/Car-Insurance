from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.auth.jwt import verify_token
from app.api.deps import get_async_session
from app.db.models.user_model import User
from app.service.user_service import UserService
from app.db.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()

async def get_current_user(session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    userService = UserService(UserRepository(session))
    user = await userService.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user
