import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from app.service.policy_service import PolicyService
from app.db.models.policy_model import InsurancePolicy

@pytest.mark.asyncio
async def test_get_policy_found():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policy = InsurancePolicy(id=1, car_id=1, start_date=None, end_date=None, provider=None, logged_expiry_at=None)
    policy_repository.get.return_value = policy
    result = await policy_service.get_policy(1)
    assert result == policy
    policy_repository.get.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_policy_not_found():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policy_repository.get.return_value = None
    result = await policy_service.get_policy(2)
    assert result is None
    policy_repository.get.assert_awaited_once_with(2)

@pytest.mark.asyncio
async def test_get_policies_by_car_id():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policies = [InsurancePolicy(id=3, car_id=2, start_date=None, end_date=None, provider=None, logged_expiry_at=None)]
    policy_repository.get_policies_by_car_id.return_value = policies
    result = await policy_service.get_policies_by_car_id(2)
    assert result == policies
    policy_repository.get_policies_by_car_id.assert_awaited_once_with(2)

@pytest.mark.asyncio
async def test_add_policy():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policy = InsurancePolicy(id=4, car_id=3, start_date=None, end_date=None, provider=None, logged_expiry_at=None)
    policy_repository.add.return_value = policy
    result = await policy_service.add_policy(policy)
    assert result == policy
    policy_repository.add.assert_awaited_once_with(policy)

@pytest.mark.asyncio
async def test_update_policy_success():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policy = InsurancePolicy(id=5, car_id=4, start_date=None, end_date=None, provider=None, logged_expiry_at=None)
    policy_repository.get.return_value = policy
    policy_repository.update.return_value = policy
    result = await policy_service.update_policy(policy)
    assert result == policy
    policy_repository.get.assert_awaited_once_with(5)
    policy_repository.update.assert_awaited_once_with(policy)

@pytest.mark.asyncio
async def test_update_policy_not_found():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policy = InsurancePolicy(id=6, car_id=5, start_date=None, end_date=None, provider=None, logged_expiry_at=None)
    policy_repository.get.return_value = None
    with pytest.raises(ValueError, match="Policy with ID 6 does not exist."):
        await policy_service.update_policy(policy)
    policy_repository.get.assert_awaited_once_with(6)

@pytest.mark.asyncio
async def test_list_policies():
    policy_repository = AsyncMock()
    policy_service = PolicyService(policy_repository)
    policies = [InsurancePolicy(id=7, car_id=6, start_date=None, end_date=None, provider=None, logged_expiry_at=None)]
    policy_repository.list.return_value = policies
    result = await policy_service.list_policies()
    assert result == policies
    policy_repository.list.assert_awaited_once()
