from dataclasses import dataclass

@dataclass(frozen=True)
class SeatBlueprint:
    seat_number: str
    class_type: str