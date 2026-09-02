from domain.entities.seat import SeatBlueprint


def generate_seat_layout(
    rows: int,
    seats_per_row: int,
    business_rows: int,
) -> list[SeatBlueprint]:
    """
    Генерирует раскладку мест для рейса на основе конфигурации самолёта.
    Первые `business_rows` рядов — бизнес-класс, остальные — эконом.
    """
    column_letters = "ABCDEFGHIJ"[:seats_per_row]
    layout = []

    for row_number in range(1, rows + 1):
        seat_class = "business" if row_number <= business_rows else "economy"
        for letter in column_letters:
            seat_number = f"{row_number}{letter}"
            layout.append(SeatBlueprint(seat_number=seat_number, class_type=seat_class))

    return layout
