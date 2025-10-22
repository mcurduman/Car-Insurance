import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from app.service.car_service import CarService
from app.db.models.car_model import Car

@pytest.mark.asyncio
async def test_get_car_found():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=1, vin="VIN123", owner_id=1)
    car_repository.get.return_value = car
    result = await car_service.get_car(1)
    assert result == car
    car_repository.get.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_car_not_found():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car_repository.get.return_value = None
    result = await car_service.get_car(2)
    assert result is None
    car_repository.get.assert_awaited_once_with(2)

@pytest.mark.asyncio
async def test_get_car_by_vin_found():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=1, vin="VIN123", owner_id=1)
    car_repository.get_car_by_vin.return_value = car
    result = await car_service.get_car_by_vin("VIN123")
    assert result == car
    car_repository.get_car_by_vin.assert_awaited_once_with("VIN123")

@pytest.mark.asyncio
async def test_add_car_success():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=2, vin="VIN456", owner_id=2)
    car_repository.get_car_by_vin.return_value = None
    car_repository.add.return_value = car
    result = await car_service.add_car(car)
    assert result == car
    car_repository.get_car_by_vin.assert_awaited_once_with("VIN456")
    car_repository.add.assert_awaited_once_with(car)

@pytest.mark.asyncio
async def test_add_car_duplicate_vin():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=3, vin="VIN789", owner_id=3)
    car_repository.get_car_by_vin.return_value = car
    with pytest.raises(ValueError, match="Car with VIN VIN789 already exists."):
        await car_service.add_car(car)
    car_repository.get_car_by_vin.assert_awaited_once_with("VIN789")

@pytest.mark.asyncio
async def test_update_car_success():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=4, vin="VIN101", owner_id=4)
    car_repository.get.return_value = car
    car_repository.update.return_value = car
    result = await car_service.update_car(car)
    assert result == car
    car_repository.get.assert_awaited_once_with(4)
    car_repository.update.assert_awaited_once_with(car)

@pytest.mark.asyncio
async def test_update_car_not_found():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=5, vin="VIN202", owner_id=5)
    car_repository.get.return_value = None
    with pytest.raises(ValueError, match="Car with ID 5 does not exist."):
        await car_service.update_car(car)
    car_repository.get.assert_awaited_once_with(5)

@pytest.mark.asyncio
async def test_update_car_vin_change():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=6, vin="VIN303", owner_id=6)
    existing_car = Car(id=6, vin="VIN404", owner_id=6)
    car_repository.get.return_value = existing_car
    with pytest.raises(ValueError, match="VIN cannot be changed."):
        await car_service.update_car(car)
    car_repository.get.assert_awaited_once_with(6)

@pytest.mark.asyncio
async def test_list_cars():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    cars = [Car(id=7, vin="VIN505", owner_id=7), Car(id=8, vin="VIN606", owner_id=8)]
    car_repository.list.return_value = cars
    result = await car_service.list_cars()
    assert result == cars
    car_repository.list.assert_awaited_once()

@pytest.mark.asyncio
async def test_list_cars_with_owner():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    cars = [Car(id=9, vin="VIN707", owner_id=9)]
    car_repository.list_with_owner.return_value = cars
    result = await car_service.list_cars_with_owner()
    assert result == cars
    car_repository.list_with_owner.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_car_success():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car = Car(id=10, vin="VIN808", owner_id=10)
    car_repository.get.return_value = car
    car_repository.delete.return_value = None
    await car_service.delete_car(10)
    car_repository.get.assert_awaited_once_with(10)
    car_repository.delete.assert_awaited_once_with(10)

@pytest.mark.asyncio
async def test_delete_car_not_found():
    car_repository = AsyncMock()
    car_service = CarService(car_repository)
    car_repository.get.return_value = None
    with pytest.raises(ValueError, match="Car with ID 11 does not exist."):
        await car_service.delete_car(11)
    car_repository.get.assert_awaited_once_with(11)
