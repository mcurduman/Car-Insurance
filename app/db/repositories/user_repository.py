from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int):
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_user_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user