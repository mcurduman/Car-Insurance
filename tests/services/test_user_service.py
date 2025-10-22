
import pytest
from unittest.mock import AsyncMock
from app.service.user_service import UserService
from app.schemas.user_schema import UserCreate

@pytest.mark.asyncio
async def test_get_user():
    repo = AsyncMock()
    repo.get_user = AsyncMock(return_value={"id": 1, "username": "testuser"})
    user_service = UserService(repo)
    result = await user_service.get_user(1)
    assert result == {"id": 1, "username": "testuser"}
    repo.get_user.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_user_by_username():
    repo = AsyncMock()
    repo.get_user_by_username = AsyncMock(return_value={"id": 1, "username": "testuser"})
    user_service = UserService(repo)
    result = await user_service.get_user_by_username("testuser")
    assert result == {"id": 1, "username": "testuser"}
    repo.get_user_by_username.assert_awaited_once_with("testuser")

@pytest.mark.asyncio
async def test_get_user_by_email():
    repo = AsyncMock()
    repo.get_user_by_email = AsyncMock(return_value={"id": 1, "email": "test@example.com"})
    user_service = UserService(repo)
    result = await user_service.get_user_by_email("test@example.com")
    assert result == {"id": 1, "email": "test@example.com"}
    repo.get_user_by_email.assert_awaited_once_with("test@example.com")

@pytest.mark.asyncio
async def test_create_user_success():
    repo = AsyncMock()
    repo.get_user_by_username = AsyncMock(return_value=None)
    repo.get_user_by_email = AsyncMock(return_value=None)
    repo.create_user = AsyncMock(return_value={"id": 2, "username": "newuser"})
    user_service = UserService(repo)
    user = UserCreate(username="newuser", email="new@example.com", password="pass")
    result = await user_service.create_user(user)
    assert result == {"id": 2, "username": "newuser"}
    repo.create_user.assert_awaited_once_with(user)

@pytest.mark.asyncio
async def test_create_user_username_taken():
    repo = AsyncMock()
    repo.get_user_by_username = AsyncMock(return_value={"id": 1, "username": "existinguser"})
    repo.get_user_by_email = AsyncMock(return_value=None)
    user_service = UserService(repo)
    user = UserCreate(username="existinguser", email="new@example.com", password="pass")
    with pytest.raises(ValueError) as exc:
        await user_service.create_user(user)
    assert "Username existinguser is already taken." in str(exc.value)

@pytest.mark.asyncio
async def test_create_user_email_taken():
    repo = AsyncMock()
    repo.get_user_by_username = AsyncMock(return_value=None)
    repo.get_user_by_email = AsyncMock(return_value={"id": 1, "email": "existing@example.com"})
    user_service = UserService(repo)
    user = UserCreate(username="newuser", email="existing@example.com", password="pass")
    with pytest.raises(ValueError) as exc:
        await user_service.create_user(user)
    assert "Email existing@example.com is already registered." in str(exc.value)