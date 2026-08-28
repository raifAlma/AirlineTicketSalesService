from dataclasses import dataclass


class InvalidAirportCode(ValueError):
    pass


class InvalidAirportField(ValueError):
    pass


@dataclass(frozen=True)
class AirportCreateData:
    code: str
    name: str
    city: str
    country: str

    def __post_init__(self):
        self._validate_code()
        self._validate_length("name", self.name)
        self._validate_length("city", self.city)
        self._validate_length("country", self.country)

    def _validate_code(self):
        if not (len(self.code) == 3 and self.code.isalpha() and self.code.isupper()):
            raise InvalidAirportCode(
                f"Airport code must be exactly 3 uppercase letters, got {self.code!r}"
            )

    def _validate_length(self, field_name: str, value: str):
        if not (1 <= len(value) <= 100):
            raise InvalidAirportField(
                f"{field_name} must be between 1 and 100 characters, got {len(value)}"
            )

@dataclass(frozen=True)
class AirportUpdateData:
    code: str | None
    name: str | None
    city: str | None
    country: str | None

    def __post_init__(self):
        if self.code is not None:
            self._validate_code()
        if self.name is not None:
            self._validate_length("name", self.name)
        if self.city is not None:
            self._validate_length("city", self.city)
        if self.country is not None:
            self._validate_length("country", self.country)

    def _validate_code(self):
        if not (len(self.code) == 3 and self.code.isalpha() and self.code.isupper()):
            raise InvalidAirportCode(
                f"Airport code must be exactly 3 uppercase letters, got {self.code!r}"
            )

    def _validate_length(self, field_name: str, value: str):
        if not (1 <= len(value) <= 100):
            raise InvalidAirportField(
                f"{field_name} must be between 1 and 100 characters, got {len(value)}"
            )


