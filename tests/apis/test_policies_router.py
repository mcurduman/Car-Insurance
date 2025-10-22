import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.oauth2 import get_current_user
from datetime import date

app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "testuser"}

@pytest.mark.asyncio
async def test_create_policy_for_car_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return {"id": car_id}
    class PolicyObj:
        def __init__(self, id, car_id, provider, start_date, end_date, logged_expiry_at=None):
            self.id = id
            self.car_id = car_id
            self.provider = provider
            self.start_date = start_date
            self.end_date = end_date
            self.logged_expiry_at = logged_expiry_at
    class FakePolicyService:
        async def add_policy(self, policy):
            return PolicyObj(10, policy.car_id, policy.provider, policy.start_date, policy.end_date, policy.logged_expiry_at)
    from app.api.deps import get_car_service, get_policy_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_policy_service] = lambda: FakePolicyService()
    transport = ASGITransport(app=app)
    today = date.today()
    tomorrow = today.replace(day=today.day + 1)
    policy_data = {
        "carId": 1,
        "provider": "TestProvider",
        "startDate": today.isoformat(),
        "endDate": tomorrow.isoformat(),
        "loggedExpiryAt": None
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/1/policies/", json=policy_data)
    assert response.status_code == 201
    assert response.json()["id"] == 10
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_policy_service)

@pytest.mark.asyncio
async def test_create_policy_for_car_404_car_override():
    class FakeCarService:
        async def get_car(self, car_id):
            return None
    class FakePolicyService:
        async def add_policy(self, policy):
            return None
    from app.api.deps import get_car_service, get_policy_service
    app.dependency_overrides[get_car_service] = lambda: FakeCarService()
    app.dependency_overrides[get_policy_service] = lambda: FakePolicyService()
    transport = ASGITransport(app=app)
    today = date.today()
    tomorrow = today.replace(day=today.day + 1)
    policy_data = {
        "carId": 999,
        "provider": "TestProvider",
        "startDate": today.isoformat(),
        "endDate": tomorrow.isoformat(),
        "loggedExpiryAt": None
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/999/policies/", json=policy_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"
    app.dependency_overrides.pop(get_car_service)
    app.dependency_overrides.pop(get_policy_service)

@pytest.mark.asyncio
async def test_get_policy_for_car_return_override():
    class PolicyObj:
        def __init__(self, id, car_id, provider, start_date, end_date, logged_expiry_at=None):
            self.id = id
            self.car_id = car_id
            self.provider = provider
            self.start_date = start_date
            self.end_date = end_date
            self.logged_expiry_at = logged_expiry_at
    class FakePolicyService:
        async def get_policy(self, policy_id):
            today = date.today()
            return PolicyObj(policy_id, 1, "TestProvider", today, today, None)
    from app.api.deps import get_policy_service
    app.dependency_overrides[get_policy_service] = lambda: FakePolicyService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/policies/10")
    assert response.status_code == 200
    assert response.json()["id"] == 10
    app.dependency_overrides.pop(get_policy_service)

@pytest.mark.asyncio
async def test_get_policy_for_car_404_override():
    class PolicyObj:
        def __init__(self, id, car_id, provider, start_date, end_date, logged_expiry_at=None):
            self.id = id
            self.car_id = car_id
            self.provider = provider
            self.start_date = start_date
            self.end_date = end_date
            self.logged_expiry_at = logged_expiry_at
    class FakePolicyService:
        async def get_policy(self, policy_id):
            today = date.today()
            return PolicyObj(policy_id, 999, "TestProvider", today, today, None)
    from app.api.deps import get_policy_service
    app.dependency_overrides[get_policy_service] = lambda: FakePolicyService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/policies/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Policy not found for this car"
    app.dependency_overrides.pop(get_policy_service)

@pytest.mark.asyncio
async def test_list_policies_for_car_override():
    class PolicyObj:
        def __init__(self, id, car_id, provider, start_date, end_date, logged_expiry_at=None):
            self.id = id
            self.car_id = car_id
            self.provider = provider
            self.start_date = start_date
            self.end_date = end_date
            self.logged_expiry_at = logged_expiry_at
    class FakePolicyService:
        async def get_policies_by_car_id(self, car_id):
            today = date.today()
            return [PolicyObj(1, car_id, "TestProvider", today, today, None), PolicyObj(2, car_id, "TestProvider", today, today, None)]
    from app.api.deps import get_policy_service
    app.dependency_overrides[get_policy_service] = lambda: FakePolicyService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/1/policies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["id"] == 1
    app.dependency_overrides.pop(get_policy_service)
