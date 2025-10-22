import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from app.service.claim_service import ClaimService
from app.db.models.claim_model import Claim

@pytest.mark.asyncio
async def test_get_claim_found():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claim = Claim(id=1, car_id=1, amount=1000.0, claim_date=None, description=None, created_at=None)
    claim_repository.get.return_value = claim
    result = await claim_service.get_claim(1)
    assert result == claim
    claim_repository.get.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_claim_not_found():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claim_repository.get.return_value = None
    result = await claim_service.get_claim(2)
    assert result is None
    claim_repository.get.assert_awaited_once_with(2)

@pytest.mark.asyncio
async def test_get_claims_by_car_id():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claims = [Claim(id=3, car_id=2, amount=500.0, claim_date=None, description=None, created_at=None)]
    claim_repository.get_by_car_id.return_value = claims
    result = await claim_service.get_claims_by_car_id(2)
    assert result == claims
    claim_repository.get_by_car_id.assert_awaited_once_with(2)

@pytest.mark.asyncio
async def test_get_claims_by_owner_id():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claims = [Claim(id=4, car_id=3, amount=750.0, claim_date=None, description=None, created_at=None)]
    claim_repository.get_by_owner_id.return_value = claims
    result = await claim_service.get_claims_by_owner_id(2)
    assert result == claims
    claim_repository.get_by_owner_id.assert_awaited_once_with(2)

@pytest.mark.asyncio
async def test_add_claim():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claim = Claim(id=5, car_id=4, amount=1200.0, claim_date=None, description=None, created_at=None)
    claim_repository.add.return_value = claim
    result = await claim_service.add_claim(claim)
    assert result == claim
    claim_repository.add.assert_awaited_once_with(claim)

@pytest.mark.asyncio
async def test_update_claim_success():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claim = Claim(id=6, car_id=5, amount=1300.0, claim_date=None, description=None, created_at=None)
    claim_repository.get.return_value = claim
    claim_repository.update.return_value = claim
    result = await claim_service.update_claim(claim)
    assert result == claim
    claim_repository.get.assert_awaited_once_with(6)
    claim_repository.update.assert_awaited_once_with(claim)

@pytest.mark.asyncio
async def test_update_claim_not_found():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claim = Claim(id=7, car_id=6, amount=1400.0, claim_date=None, description=None, created_at=None)
    claim_repository.get.return_value = None
    with pytest.raises(ValueError, match="Claim with ID 7 does not exist."):
        await claim_service.update_claim(claim)
    claim_repository.get.assert_awaited_once_with(7)

@pytest.mark.asyncio
async def test_list_claims():
    claim_repository = AsyncMock()
    claim_service = ClaimService(claim_repository)
    claims = [Claim(id=8, car_id=7, amount=1500.0, claim_date=None, description=None, created_at=None)]
    claim_repository.list.return_value = claims
    result = await claim_service.list_claims()
    assert result == claims
    claim_repository.list.assert_awaited_once()
