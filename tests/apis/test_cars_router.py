import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.oauth2 import get_current_user
from app.db.models.owner_model import Owner
from app.api.deps import get_async_session
from app.db.models.user_model import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
import uuid

# Dependency override for authentication
def override_get_current_user():
    return {"id": 1, "username": "testuser"}
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

# Fixture to ensure owner exists
@pytest.fixture(scope="module", autouse=True)
async def setup_owner():
    transport = ASGITransport(app=app)
    owner_data = {"name": "Test Owner", "email": "testowner@example.com"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/api/owners/", json=owner_data)

# Fixture to create owner directly in DB and provide its id
@pytest.fixture(scope="module")
async def owner_id(test_user):
    transport = ASGITransport(app=app)
    owner_data = {
        "name": "Test Owner",
        "email": test_user.email
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/owners/", json=owner_data)
        owner = response.json()
        return owner["id"]

# Fixture to mock a user in the test database
@pytest.fixture(scope="module")
async def test_user():
    async for session in get_async_session():
        user_repo = UserRepository(session)
        existing_user = await user_repo.get_user_by_username("string")
        if existing_user:
            return existing_user
        user_data = UserCreate(username="string", email="user@example.com", password="testpassword")
        user = await user_repo.create_user(user_data)
        return user



@pytest.mark.asyncio
async def test_list_cars():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_car_success(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": str(uuid.uuid4()).replace("-", "")[:17],
        "make": "Honda",
        "model": "Accord",
        "yearOfManufacture": 2022,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/", json=car_data)
        if response.status_code != 201:
            print("Car creation failed:", response.status_code, response.json())
        assert response.status_code == 201
        assert response.json()["vin"] == car_data["vin"].upper()
        car_id = response.json().get("id")
        assert car_id is not None

@pytest.mark.asyncio
async def test_create_car_duplicate_vin(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": "1HGCM82633A004353",
        "make": "Toyota",
        "model": "Corolla",
        "yearOfManufacture": 2021,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # First create
        await ac.post("/api/cars/", json=car_data)
        # Duplicate VIN
        response = await ac.post("/api/cars/", json=car_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_car_invalid_vin(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": "SHORTVIN",
        "make": "Ford",
        "model": "Focus",
        "yearOfManufacture": 2019,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/", json=car_data)
    assert response.status_code == 422 or response.status_code == 400

@pytest.mark.asyncio
async def test_get_car_success(owner_id):
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
        if create_resp.status_code != 201:
            print("Car creation failed:", create_resp.status_code, create_resp.json())
        car_id = create_resp.json().get("id")
        assert car_id is not None
        response = await ac.get(f"/api/cars/{car_id}")
    assert response.status_code == 200
    assert response.json()["vin"] == car_data["vin"].upper()

@pytest.mark.asyncio
async def test_get_car_by_vin_success(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": "1HGCM82633A004355",
        "make": "BMW",
        "model": "X5",
        "yearOfManufacture": 2023,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/api/cars/", json=car_data)
        response = await ac.get(f"/api/cars/by-vin/{car_data['vin']}")
    assert response.status_code == 200
    assert response.json()["vin"] == car_data["vin"]

@pytest.mark.asyncio
async def test_get_car_by_vin_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/by-vin/NOTEXISTVIN1234567")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

@pytest.mark.asyncio
async def test_delete_car_success(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": str(uuid.uuid4()).replace("-", "")[:17],
        "make": "Kia",
        "model": "Ceed",
        "yearOfManufacture": 2025,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_resp = await ac.post("/api/cars/", json=car_data)
        if create_resp.status_code != 201:
            print("Car creation failed:", create_resp.status_code, create_resp.json())
        car_id = create_resp.json().get("id")
        assert car_id is not None
        response = await ac.delete(f"/api/cars/{car_id}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_car_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/api/cars/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

@pytest.mark.asyncio
async def test_insurance_valid_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/99999/insurance-valid?date=2025-10-22")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

@pytest.mark.asyncio
async def test_insurance_valid_invalid_date(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": str(uuid.uuid4()).replace("-", "")[:17],
        "make": "Hyundai",
        "model": "i30",
        "yearOfManufacture": 2025,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_resp = await ac.post("/api/cars/", json=car_data)
        if create_resp.status_code != 201:
            print("Car creation failed:", create_resp.status_code, create_resp.json())
        car_id = create_resp.json().get("id")
        assert car_id is not None
        response = await ac.get(f"/api/cars/{car_id}/insurance-valid?date=1800-01-01")
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]

@pytest.mark.asyncio
async def test_insurance_valid_valid_false(owner_id):
    transport = ASGITransport(app=app)
    car_data = {
        "vin": str(uuid.uuid4()).replace("-", "")[:17],
        "make": "Opel",
        "model": "Astra",
        "yearOfManufacture": 2025,
        "ownerId": owner_id
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_resp = await ac.post("/api/cars/", json=car_data)
        if create_resp.status_code != 201:
            print("Car creation failed:", create_resp.status_code, create_resp.json())
        car_id = create_resp.json().get("id")
        assert car_id is not None
        response = await ac.get(f"/api/cars/{car_id}/insurance-valid?date=2025-10-22")
    assert response.status_code == 200
    assert response.json()["valid"] is False


@pytest.mark.asyncio
async def test_get_car_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"


@pytest.mark.asyncio
async def test_create_car_invalid():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/cars/", json={})
    assert response.status_code == 422
