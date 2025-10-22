import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from app.service.owner_service import OwnerService
from app.db.models.owner_model import Owner
from app.db.models.car_model import Car
from app.db.models.claim_model import Claim
from app.db.models.policy_model import InsurancePolicy


@pytest.mark.asyncio
class TestOwnerService:
    @pytest_asyncio.fixture
    def owner_repository(self):
        repo = AsyncMock()
        return repo

    @pytest_asyncio.fixture
    def owner_service(self, owner_repository):
        return OwnerService(owner_repository)

    @pytest.mark.asyncio
    async def test_get_owner_found(self, owner_service, owner_repository):
        owner = Owner(id=1, name="Test", email="test@example.com")
        owner_repository.get.return_value = owner
        result = await owner_service.get_owner(1)
        assert result == owner
        owner_repository.get.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_get_owner_not_found(self, owner_service, owner_repository):
        owner_repository.get.return_value = None
        result = await owner_service.get_owner(2)
        assert result is None
        owner_repository.get.assert_awaited_once_with(2)

    @pytest.mark.asyncio
    async def test_add_owner(self, owner_service, owner_repository):
        owner = Owner(id=1, name="Test", email="test@example.com")
        owner_repository.add.return_value = owner
        result = await owner_service.add_owner(owner)
        assert result == owner
        owner_repository.add.assert_awaited_once_with(owner)

    @pytest.mark.asyncio
    async def test_update_owner_success(self, owner_service, owner_repository):
        owner = Owner(id=1, name="Test", email="test@example.com")
        owner_repository.get.return_value = owner
        owner_repository.update.return_value = owner
        result = await owner_service.update_owner(owner)
        assert result == owner
        owner_repository.get.assert_awaited_once_with(owner.id)
        owner_repository.update.assert_awaited_once_with(owner)

    @pytest.mark.asyncio
    async def test_update_owner_not_found(self, owner_service, owner_repository):
        owner = Owner(id=2, name="Test", email="test@example.com")
        owner_repository.get.return_value = None
        with pytest.raises(ValueError, match="Owner with ID 2 does not exist."):
            await owner_service.update_owner(owner)
        owner_repository.get.assert_awaited_once_with(owner.id)

    @pytest.mark.asyncio
    async def test_list_owners(self, owner_service, owner_repository):
        owners = [Owner(id=1, name="A", email="a@example.com"), Owner(id=2, name="B", email="b@example.com")]
        owner_repository.list.return_value = owners
        result = await owner_service.list_owners()
        assert result == owners
        owner_repository.list.assert_awaited_once()


