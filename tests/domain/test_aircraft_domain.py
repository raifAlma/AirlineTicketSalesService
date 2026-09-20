from unittest.mock import AsyncMock

import pytest

from api.schemas.aircraft import UpdateAircraftSchema
from domain.entities.aircraft import AircraftCreateData, AircraftUpdateData
from domain.validators.aircraft import validate_model, InvalidAircraftName, InvalidQuantityBusinessRows, \
    validate_business_rows
from infrastructure.database.postgresql.models import Aircraft
from usecases.aircraft.update.implementation import PostgreSQLUpdateAircraftUseCase


def test_update_airport_with_valid_data_succeeds():
    aircraft = AircraftCreateData(
        model="Airbus 222",
        rows= 30,
        seats_per_row= 5,
        business_rows=4
    )
    assert aircraft.model == "Airbus 222"
    assert aircraft.rows == 30
    assert aircraft.seats_per_row == 5
    assert aircraft.business_rows == 4

def test_create_aircraft_with_empty_model():
    with pytest.raises(InvalidAircraftName):
        AircraftCreateData(
            model="",
            rows= 30,
            seats_per_row= 5,
            business_rows=4
        )

@pytest.mark.parametrize(
    'rows, business_rows',
    [
        (-1, 0),
        (5, -1),
        (5, 6),
    ],
)
def test_validate_business_rows_raises_error(rows, business_rows):
    with pytest.raises(InvalidQuantityBusinessRows):
        validate_business_rows(rows, business_rows)



async def test_update_aircraft_usecase_calls_repository_correctly():

    mock_repository = AsyncMock()
    mock_repository.update.return_value = "Aircraft(fake result)"

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.repository = mock_repository

    usecase = PostgreSQLUpdateAircraftUseCase(uow=mock_uow)
    payload = UpdateAircraftSchema(
        model="Aircraft 222")
    aircraft_id = 'aircraft-id-123'
    await usecase.execute(aircraft_id, payload)
    expected = AircraftUpdateData(
        model="Aircraft 222",
        rows=None,
        seats_per_row=None,
        business_rows=None
    )
    mock_repository.update.assert_called_once_with(aircraft_id, expected)