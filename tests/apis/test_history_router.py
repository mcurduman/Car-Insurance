import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.oauth2 import get_current_user

# Dependency override for authentication
app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "testuser"}

@pytest.mark.asyncio
async def test_get_car_history_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cars/99999/history")
    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

# Add more tests for valid car_id and edge cases as needed
