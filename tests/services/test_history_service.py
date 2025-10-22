import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from app.service.history_service import HistoryService

class DummyCar:
    def __init__(self, id):
        self.id = id

class DummyPolicy:
    def __init__(self, id, start_date, end_date, provider):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.provider = provider

class DummyClaim:
    def __init__(self, id, claim_date, amount, description):
        self.id = id
        self.claim_date = claim_date
        self.amount = amount
        self.description = description

@pytest.mark.asyncio
class TestHistoryService:
    @pytest_asyncio.fixture
    def session(self):
        return AsyncMock()

    @pytest_asyncio.fixture
    def history_service(self, session):
        return HistoryService(session)

    @pytest.mark.asyncio
    async def test_get_car_history_full(self, history_service, session):
        car = DummyCar(1)
        policies = [DummyPolicy(10, "2025-01-01", "2025-12-31", "ProviderA")]
        claims = [DummyClaim(20, "2025-06-01", 1000.0, "Accident")]
        with patch("app.db.repositories.car_repository.CarRepository.get", AsyncMock(return_value=car)), \
             patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=policies)), \
             patch("app.db.repositories.claim_repository.ClaimRepository.get_by_car_id", AsyncMock(return_value=claims)):
            history = await history_service.get_car_history(1)
            assert any(item["type"] == "POLICY" for item in history)
            assert any(item["type"] == "CLAIM" for item in history)
            assert history[0]["type"] in ["POLICY", "CLAIM"]

    @pytest.mark.asyncio
    async def test_get_car_history_only_policies(self, history_service, session):
        car = DummyCar(2)
        policies = [DummyPolicy(11, "2025-01-01", "2025-12-31", "ProviderB")]
        claims = []
        with patch("app.db.repositories.car_repository.CarRepository.get", AsyncMock(return_value=car)), \
             patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=policies)), \
             patch("app.db.repositories.claim_repository.ClaimRepository.get_by_car_id", AsyncMock(return_value=claims)):
            history = await history_service.get_car_history(2)
            assert all(item["type"] == "POLICY" for item in history)

    @pytest.mark.asyncio
    async def test_get_car_history_only_claims(self, history_service, session):
        car = DummyCar(3)
        policies = []
        claims = [DummyClaim(21, "2025-07-01", 500.0, "Scratch")]
        with patch("app.db.repositories.car_repository.CarRepository.get", AsyncMock(return_value=car)), \
             patch("app.db.repositories.policy_repository.PolicyRepository.get_policies_by_car_id", AsyncMock(return_value=policies)), \
             patch("app.db.repositories.claim_repository.ClaimRepository.get_by_car_id", AsyncMock(return_value=claims)):
            history = await history_service.get_car_history(3)
            assert all(item["type"] == "CLAIM" for item in history)

    @pytest.mark.asyncio
    async def test_get_car_history_car_not_found(self, history_service, session):
        with patch("app.db.repositories.car_repository.CarRepository.get", AsyncMock(return_value=None)):
            history = await history_service.get_car_history(999)
            assert history is None
