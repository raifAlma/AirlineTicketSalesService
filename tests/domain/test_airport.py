import pytest

from src.domain.entities.airport import AirportCreateData, InvalidAirportCode, InvalidAirportField


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