import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from datetime import date
from app.service.validity_service import ValidityService

class DummyPolicy:
    def __init__(self, start_date, end_date, logged_expiry_at=None):
        self.start_date = start_date
        self.end_date = end_date
        self.logged_expiry_at = logged_expiry_at

@pytest.mark.asyncio
class TestValidityService:
    @pytest_asyncio.fixture
    def session(self):
        return AsyncMock()

    @pytest_asyncio.fixture
    def validity_service(self, session):
        return ValidityService(session)

    @pytest.mark.asyncio
    async def test_is_valid_true(self, validity_service, session):
        valid_policy = DummyPolicy(date(2025, 1, 1), date(2025, 12, 31))
        with patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=[valid_policy])):
            result = await validity_service.is_valid(1, date(2025, 6, 1))
            assert result is True

    @pytest.mark.asyncio
    async def test_is_valid_false_no_policies(self, validity_service, session):
        with patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=[])):
            result = await validity_service.is_valid(1, date(2025, 6, 1))
            assert result is False

    @pytest.mark.asyncio
    async def test_is_valid_false_expired_policies(self, validity_service, session):
        expired_policy = DummyPolicy(date(2024, 1, 1), date(2024, 12, 31), logged_expiry_at=date(2024, 12, 31))
        with patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=[expired_policy])):
            result = await validity_service.is_valid(1, date(2025, 6, 1))
            assert result is False

    @pytest.mark.asyncio
    async def test_is_valid_false_outside_interval(self, validity_service, session):
        policy = DummyPolicy(date(2025, 1, 1), date(2025, 3, 31))
        with patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=[policy])):
            result = await validity_service.is_valid(1, date(2025, 6, 1))
            assert result is False
