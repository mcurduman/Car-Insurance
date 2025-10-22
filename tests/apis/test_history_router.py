import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.oauth2 import get_current_user
import uuid
from app.db.models.owner_model import Owner
from app.db.models.policy_model import InsurancePolicy
from app.db.models.claim_model import Claim
from app.api.deps import get_async_session
from datetime import date
from unittest.mock import AsyncMock

app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "testuser"}

@pytest.fixture(scope="module")
async def owner_id():
    async for session in get_async_session():
        owner = Owner(name="Test Owner", email="testowner@example.com")
        session.add(owner)
        await session.commit()
        await session.refresh(owner)
        return owner.id

@pytest.mark.asyncio
async def test_get_car_history_empty(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": str(uuid.uuid4()).replace("-", "")[:17],
        "make": "Mazda",
        "model": "3",
        "yearOfManufacture": 2023,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_resp = await ac.post("/api/cars/", json=car_data)
        car_id = create_resp.json().get("id")
        assert car_id is not None
        response = await ac.get(f"/api/cars/{car_id}/history")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_car_history_success(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": str(uuid.uuid4()).replace("-", "")[:17],
        "make": "Toyota",
        "model": "Corolla",
        "yearOfManufacture": 2021,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_resp = await ac.post("/api/cars/", json=car_data)
        car_id = create_resp.json().get("id")
        assert car_id is not None
    # Creează polița direct în DB
    from app.db.models.policy_model import InsurancePolicy
    from app.api.deps import get_async_session
    async for session in get_async_session():
        policy = InsurancePolicy(car_id=car_id, provider="TestProvider", start_date=date(2021, 1, 1), end_date=date(2022, 1, 1))
        session.add(policy)
        await session.commit()
        await session.refresh(policy)
    # Creează o daună direct în DB
    from app.db.models.claim_model import Claim
    async for session in get_async_session():
        claim = Claim(car_id=car_id, amount=1000.0, description="Test claim", claim_date=date(2021, 6, 15))
        session.add(claim)
        await session.commit()
        await session.refresh(claim)
    # Verifică istoricul
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/api/cars/{car_id}/history")
    assert response.status_code == 200
    history = response.json()
    assert any(h["type"] == "POLICY" for h in history)
    assert any(h["type"] == "CLAIM" for h in history)

@pytest.mark.asyncio
async def test_get_car_history_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/999999/history")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

@pytest.mark.asyncio
async def test_get_car_history_404_override():
    class FakeHistoryService:
        async def get_car_history(self, car_id):
            return None
    from app.api.deps import get_history_service
    app.dependency_overrides[get_history_service] = lambda: FakeHistoryService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/12345/history")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"
    app.dependency_overrides.pop(get_history_service)

@pytest.mark.asyncio
async def test_get_car_history_return_override():
    class FakeHistoryService:
        async def get_car_history(self, car_id):
            return [{"type": "POLICY", "info": "test policy"}]
    from app.api.deps import get_history_service
    app.dependency_overrides[get_history_service] = lambda: FakeHistoryService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/12345/history")
    assert response.status_code == 200
    assert response.json() == [{"type": "POLICY", "info": "test policy"}]
    app.dependency_overrides.pop(get_history_service)
