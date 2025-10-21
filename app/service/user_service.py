from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate
from app.db.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int):
        return await self.user_repository.get_user(user_id)

    async def get_user_by_username(self, username: str):
        return await self.user_repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        return await self.user_repository.get_user_by_email(email)

    async def create_user(self, user: UserCreate):
        if await self.get_user_by_username(user.username):
            raise ValueError(f"Username {user.username} is already taken.")
        if await self.get_user_by_email(user.email):
            raise ValueError(f"Email {user.email} is already registered.")
        return await self.user_repository.create_user(user)
