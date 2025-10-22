import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.oauth2 import get_current_user
from app.schemas.owner_schema import OwnerCreate, OwnerUpdate
from unittest.mock import AsyncMock

app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "testuser"}

@pytest.mark.asyncio
async def test_list_owners_override():
    class FakeOwnerService:
        async def list_owners(self):
            return [{"id": 1, "name": "Test Owner", "email": "testowner@example.com"}]
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/owners/")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test Owner"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_get_owner_404_override():
    class FakeOwnerService:
        async def get_owner(self, owner_id):
            return None
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/owners/12345")
    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_get_owner_return_override():
    class FakeOwnerService:
        async def get_owner(self, owner_id):
            return {"id": owner_id, "name": "Test Owner", "email": "testowner@example.com"}
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/owners/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Owner"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_create_owner_override():
    class OwnerObj:
        def __init__(self, id, name, email):
            self.id = id
            self.name = name
            self.email = email
    class FakeOwnerService:
        async def add_owner(self, owner):
            return OwnerObj(2, owner.name, owner.email)
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    owner_data = {"name": "New Owner", "email": "newowner@example.com"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/owners/", json=owner_data)
    assert response.status_code == 201
    assert response.json()["name"] == "New Owner"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_create_owner_400_override():
    class FakeOwnerService:
        async def add_owner(self, owner):
            raise ValueError("Owner already exists")
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    owner_data = {"name": "New Owner", "email": "newowner@example.com"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/owners/", json=owner_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Owner already exists"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_update_owner_404_override():
    class FakeOwnerService:
        async def get_owner(self, owner_id):
            return None
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    owner_update = {"name": "Updated Owner"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/api/owners/12345", json=owner_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_update_owner_400_override():
    class FakeOwnerService:
        async def get_owner(self, owner_id):
            class OwnerObj:
                def __init__(self):
                    self.id = owner_id
                    self.name = "Old Name"
                    self.email = "old@example.com"
            return OwnerObj()
        async def update_owner(self, owner):
            raise ValueError("Invalid update")
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    owner_update = {"name": "Updated Owner"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/api/owners/1", json=owner_update)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid update"
    app.dependency_overrides.pop(get_owner_service)

@pytest.mark.asyncio
async def test_update_owner_success_override():
    class FakeOwnerService:
        async def get_owner(self, owner_id):
            class OwnerObj:
                def __init__(self):
                    self.id = owner_id
                    self.name = "Old Name"
                    self.email = "old@example.com"
            return OwnerObj()
        async def update_owner(self, owner):
            return {"id": owner.id, "name": owner.name, "email": owner.email}
    from app.api.deps import get_owner_service
    app.dependency_overrides[get_owner_service] = lambda: FakeOwnerService()
    transport = ASGITransport(app=app)
    owner_update = {"name": "Updated Owner"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/api/owners/1", json=owner_update)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Owner"
    app.dependency_overrides.pop(get_owner_service)
