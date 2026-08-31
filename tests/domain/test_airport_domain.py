from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from api.schemas.airport import UpdateAirportSchema
from src.domain.entities.airport import (
    AirportCreateData,
    AirportUpdateData,
    InvalidAirportCode,
    InvalidAirportField,
)
from usecases.airport.get.implementation import PostgreSQLGetAirportUseCase
from usecases.airport.update.implementation import PostgreSQLUpdateAirportUseCase


def test_create_airport_with_valid_data_succeeds():
    # Arrange — готовим валидные данные
    code = "LHR"
    name = "Heathrow"
    city = "London"
    country = "UK"

    # Act — выполняем то, что тестируем
    airport = AirportCreateData(code=code, name=name, city=city, country=country)

    # Assert — проверяем, что результат правильный
    assert airport.code == "LHR"
    assert airport.name == "Heathrow"
    assert airport.city == "London"
    assert airport.country == "UK"


def test_create_airport_with_lowercase_code_raises_error():
    # Arrange + Act + Assert объединены через pytest.raises
    with pytest.raises(InvalidAirportCode):
        AirportCreateData(code="lhr", name="Heathrow", city="London", country="UK")


def test_create_airport_with_empty_city_raises_error():
    with pytest.raises(InvalidAirportField):
        AirportCreateData(code="HDH", name="simf", city="", country="UK")


@pytest.mark.parametrize(
    "field_name, kwargs",
    [
        ("city", {"code": "HDH", "name": "simf", "city": "", "country": "UK"}),
        ("name", {"code": "HDH", "name": "", "city": "London", "country": "UK"}),
        ("country", {"code": "HDH", "name": "simf", "city": "London", "country": ""}),
    ],
)
def test_create_airport_with_empty_field_raises_error(field_name, kwargs):
    with pytest.raises(InvalidAirportField):
        AirportCreateData(**kwargs)


def test_create_airport_with_city_101_symbols_raises_error():
    with pytest.raises(InvalidAirportField):
        AirportCreateData(code="AAA", name="Heathrow", city="A" * 101, country="UK")


async def test_update_airport_usecase_calls_repository_correctly():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.update.return_value = "Airport(fake result)"

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.repository = mock_repo

    usecase = PostgreSQLUpdateAirportUseCase(uow=mock_uow)
    payload = UpdateAirportSchema(name="New Heathrow")
    airport_id = "airport-id-123"

    # Act
    result = await usecase.execute(airport_id, payload)

    # Assert
    expected_data = AirportUpdateData(
        code=None, name="New Heathrow", city=None, country=None
    )
    mock_repo.update.assert_called_once_with(airport_id, expected_data)
