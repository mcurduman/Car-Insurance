import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.oauth2 import get_current_user
from datetime import date

app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "testuser"}

@pytest.mark.asyncio
async def test_create_claim_for_car_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return {"id": car_id}
    class ClaimObj:
        def __init__(self, id, car_id, claim_date, description, amount):
            self.id = id
            self.car_id = car_id
            self.claim_date = claim_date
            self.description = description
            self.amount = amount
    class FakeClaimService:
        async def add_claim(self, claim):
            return ClaimObj(10, claim.car_id, claim.claim_date, claim.description, claim.amount)
    from app.api.deps import get_car_service, get_claim_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_claim_service] = lambda: FakeClaimService()
    transport = ASGITransport(app=app)
    claim_data = {
        "carId": 1,
        "claimDate": date.today().isoformat(),
        "description": "Test claim",
        "amount": 100.0
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/1/claims/", json=claim_data)
    assert response.status_code == 201
    assert response.json()["id"] == 10
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_claim_service)

@pytest.mark.asyncio
async def test_get_claim_for_car_return_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return {"id": car_id}
    class ClaimObj:
        def __init__(self, id, car_id):
            self.id = id
            self.car_id = car_id
    class FakeClaimService:
        async def get_claim(self, claim_id):
            return ClaimObj(claim_id, 1)
    from app.api.deps import get_car_service, get_claim_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_claim_service] = lambda: FakeClaimService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/claims/10")
    assert response.status_code == 200
    assert response.json()["id"] == 10
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_claim_service)

@pytest.mark.asyncio
async def test_get_claim_for_car_404_car_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return None
    class FakeClaimService:
        async def get_claim(self, claim_id):
            return None
    from app.api.deps import get_car_service, get_claim_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_claim_service] = lambda: FakeClaimService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/claims/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_claim_service)

@pytest.mark.asyncio
async def test_get_claim_for_car_404_claim_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return {"id": car_id}
    class FakeClaimService:
        async def get_claim(self, claim_id):
            return None
    from app.api.deps import get_car_service, get_claim_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_claim_service] = lambda: FakeClaimService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/claims/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found for this car"
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_claim_service)

@pytest.mark.asyncio
async def test_get_claim_for_car_404_claim_wrong_car_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return {"id": car_id}
    class ClaimObj:
        def __init__(self, id, car_id):
            self.id = id
            self.car_id = 999 # alt car_id
    class FakeClaimService:
        async def get_claim(self, claim_id):
            return ClaimObj(claim_id, 999)
    from app.api.deps import get_car_service, get_claim_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_claim_service] = lambda: FakeClaimService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/claims/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found for this car"
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_claim_service)

@pytest.mark.asyncio
async def test_create_claim_for_car_404_car_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return None
    class FakeClaimService:
        async def add_claim(self, claim):
            return None
    from app.api.deps import get_car_service, get_claim_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_claim_service] = lambda: FakeClaimService()
    transport = ASGITransport(app=app)
    claim_data = {
        "carId": 999,
        "claimDate": date.today().isoformat(),
        "description": "Test claim",
        "amount": 100.0
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/999/claims/", json=claim_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_claim_service)
